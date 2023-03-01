from __future__ import division

try:
    import argparse, pathlib, csv
    import matplotlib.pyplot as plt
    import statistics
except ImportError as e:
    print(e)

def main():
    args = parser.parse_args()

    # OPEN THE CSV-FILE WITH DATA
    with open(args.file, mode='r', encoding="UTF-8") as csv_data:
        artifactData = csv.DictReader(csv_data)
        contextNumbers = set()
        contexts = {}
        
        # STORE ARTIFACTS IN MEMORY, ORGANIZED BY BURIAL NUMBER
        for artifact in artifactData:

            # FILTER OUT MESA'EED RELATED CONTEXTS ONLY
            try:
                if "Mesa’eed" in artifact['Site.string()'] and artifact['Grave.string()'] is not "" and "?" not in artifact['Grave.string()']:
                    contextNumbers.add(artifact['Grave.string()'])

                    # ADD A NEW BURIAL ENTRY
                    if artifact['Grave.string()'] not in contexts.keys(): contexts[artifact['Grave.string()']] = []

                    # BURIAL ALREADY EXISTS: ADD ARTIFACT TO OTHER ARTIFACTS FROM THIS BURIAL
                    contexts[artifact['Grave.string()']].append(artifact)
            except:
                print("error")

        contextNumbers = list(filter(None, contextNumbers))

        with open('SD.csv', mode='w') as csvfile:
            fieldnames = ['Context', 'min', 'max', 'Q1', 'Q2', 'Q3']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for context in contexts.keys():
                try:
                    minVals, maxVals, allVals = [], [], []
                    for artifact in contexts[context]:
                        if artifact['SD_MIN'].isdigit(): minVals.append(int(artifact['SD_MIN']))
                        if artifact['SD_MAX'].isdigit(): maxVals.append(int(artifact['SD_MAX']))
                    allVals = minVals + maxVals
                    allVals.sort()
                    if (len(allVals) > 1):
                        
                        # DEFINE ALL VALUES
                        minVal = min(allVals)
                        maxVal = max(allVals)
                        q1 = statistics.median(allVals[:len(allVals)//2])
                        q2 = statistics.median(allVals)
                        q3 = statistics.median(allVals[len(allVals)//2:])
                        data = (minVal, maxVal, q1, q2, q3)

                        # WRITE VALUES TO CSV-FILE
                        writer.writerow({'Context': context.replace('M/', ''), 'min': str(minVal), 'max' : str(maxVal), 'Q1' : str(q1), 'Q2' : str(q2), 'Q3' : str(q3) })
                        
                        fig1, ax1 = plt.subplots()

                        # THESE ARE THE PHASES DEFINED BY PETRIE & KAISER EXPRESSED IN SEQUENCE DATES
                        # NOTE: SEQUENCE DATE VALUES FOR KAISER ARE NOT BASED ON SPECIFIC ARTIFACT TYPES, BUT SIMPLY ON HIS OWN PUBLISHED RANGES (KAISER 1956; 1957)
                        # TODO: BUILDING THIS PROGRAM AROUND SPECIFIC ARTIFACT TYPES WILL REQUIRE DEFINING A MATRIX WITH TYPES, ASSIGNING SEQUENCE DATES AND PHASES PER AUTHOR
                        petrie = [(30, 37, 0.1), (37, 60, 0.2), (60, 75, 0.3), (75, 80, 0.4)]
                        kaiser = [(30, 38, 0.1), (38, 45, 0.2), (45, 63, 0.3), (63, 80, 0.4)]
                        
                        # THE PHASES BY STAN HENDRICKX (2006)
                        # THESE ARE PHASES DEFINED BY HENDRICKX WITH SPECIFIC CERAMIC TYPES. THESE ARE NOT IMPLEMENTED AT THE MOMENT
                        # hendrickx = {
                        #     'NQIA' : 'B18d, B21b, B22b, B22d, B22f, C10e, C10l, C10N, C64b, C64n, C76h',
                        #     'NQIB' : 'B18b, B18c, B21c, B21d2, B22j, B25b, B25c, B26b, C4h, C5d, C5m, F11a, P1a, P11a,P17, C75b, C76d, C76w'
                        #     'NQIC' : 'B27a, B27f, B35a, B26a, B26b, B26c, B55b, B57a, B57b, B58b, B58c, B62b, B62c, B62d, B77a, B71b, B74a, B74b, B79a, B92a, B92b, P56a, P56b, C24, C26l, C27n, C30h, C53, C54'
                        #     'NQIIA' : 'R65b, R65c, R66a, R66p, R69c, R69d, B35b, B37b, B38c, B50, B53a, B53b'
                        #     'NQIIB' : 'B25, B27, B35, B41, B44, B56, B57, B58, B62, B63, B64, B65, B66, B67, B68, R1–36,
                        #     # R 62–69
                        #     # R 80–86
                        # }

                        # DEFINE A GRAPH IN PETRIE'S SEQUENCE DATING SPACE
                        ax1.set_title(context)
                        for period in petrie:
                            plt.axvspan(period[0], period[1], facecolor=f"{period[2]}")
                        ax1.set_xlabel('Period (Petrie)')
                        ax1.set_xlim(30, 80)
                        ax1.set_xticks([30, 40, 50, 60, 70, 80])
                        ax1.boxplot(data, vert=False)

                        # SAVE THE FIRST PLOT IN PETRIE'S SEQUENCE DATING SPACE
                        plt.savefig(f"output/{context.replace('/', '_')}-Petrie.png")
                        
                        # DEFINE A GRAPH IN KAISER'S SEQUENCE DATING SPACE
                        ax1.set_title(context)
                        for period in kaiser:
                            plt.axvspan(period[0], period[1], facecolor=f"{period[2]}")
                        ax1.set_xlabel('Period (Kaiser)')
                        ax1.set_xlim(30, 80)
                        ax1.set_xticks([30, 40, 50, 60, 70, 80])
                        ax1.boxplot(data, vert=False)
                        
                        # SAVE THE SECOND PLOT IN KAISER'S SEQUENCE DATING SPACE
                        plt.savefig(f"output/{context.replace('/', '_')}-Kaiser.png")

                        # TODO: DEFINE A GRAPH IN HENDRICKX'S SPACE
                        # ax1.set_title(context)
                        # for period in hendrickx:
                        #     plt.axvspan(period[0], period[1], facecolor=f"{period[2]}")
                        # ax1.set_xlabel('Period (Hendrickx)')
                        # ax1.set_xlim(30, 80)
                        # ax1.set_xticks([30, 40, 50, 60, 70, 80])
                        # ax1.boxplot(data, vert=False)

                        # SAVE THE THIRD PLOT IN HENDRICKX'S SPACE
                        # plt.savefig(f"{context.replace('/', '_')}-Hendrickx.png")

                        plt.close()


                except KeyError as e:
                    print(f"{e}: No artifacts for context {context}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculate and print boxplots from sequence date numbers')
    parser.add_argument('file', metavar='file', type=pathlib.Path, help='The csv file with date ranges to process')
    main()