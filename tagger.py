# The tagger.py starter code for CSC384 A4.
# Currently reads in the names of the training files, test file and output file,
# and calls the tagger (which you need to implement)
import os
import sys

def tag(training_list, test_file, output_file):
    # Tag the words from the untagged input file and write them into the output file.
    # Doesn't do much else beyond that yet.
    print("Tagging the file.")
    #
    # YOUR IMPLEMENTATION GOES HERE
    #
    ## Need to create model from training list

    #       TAG1 TAG2 TAG3 TAG4 TAG5 TAG6 TAG7
    # WORD

    # Dict words = {word : {tag: Number of times}}
    ## Emissions table
    ## Need to account for multiple training lists btw
    ## Maybe need to keep track of total counts?
    # counts = dict()
    # corpus = open(training_list[0], "r")
    # emissions = dict()
    # total_words = 0
    # for line in corpus:
    #     total_words += 1
    #     y = line.split(":")
    #     word = y[0].strip()
    #     tag = y[1].strip()
    #     if word in emissions:
    #         if tag in emissions[word]:
    #             emissions[word][tag] += 1
    #         else:
    #             emissions[word][tag] = 1
    #     else:
    #         tags = dict()
    #         tags[tag] = 1
    #         emissions[word] = tags
    # transitions = dict()
    # ### transitions
    # ## {tag: {{prev_tag: count}, {prev_tag: count}}
    # previous_tag = "sentence_start"
    # for line in corpus:     
    #     tag = line.split(":")[1].strip()
    #     word = line.split(":")[0].strip()
    #     # tag = y[1].strip() 
    #     if previous_tag in transitions:
    #         if tag in transitions[previous_tag]:
    #             transitions[previous_tag][tag] += 1
    #         else:
    #              transitions[previous_tag][tag] = 1
    #     else:
    #         transitions[previous_tag] = {tag: 1}
    #     if (word == "." or word == "?" or word =="!"):
    #         previous_tag = "sentence_start"
    #     else:
    #         previous_tag = tag
    total_words = 0
    counts = dict()
    counts["sentence_start"] = 0
    emissions = dict()
    transitions = dict()
    ## need to normalize everything
    for file in training_list:
        corpus = open(file, "r")
        previous_tag = "sentence_start"
        for line in corpus:
            total_words += 1
            y = line.split(":")
            word = y[0].strip()
            tag = y[1].strip()
            if tag in counts:
                counts[tag] += 1
            else:
                counts[tag] = 1
            if word in emissions:
                if tag in emissions[word]:
                    emissions[word][tag] += 1
                else:
                    emissions[word][tag] = 1
            else:
                tags = dict()
                tags[tag] = 1
                emissions[word] = tags
            if previous_tag in transitions:
                if tag in transitions[previous_tag]:
                    transitions[previous_tag][tag] += 1
                else:
                    transitions[previous_tag][tag] = 1
            else:
                transitions[previous_tag] = {tag: 1}
            if (word == "." or word == "?" or word =="!"):
                counts["sentence_start"] += 1
                previous_tag = "sentence_start"
            else:
                previous_tag = tag
        corpus.close()

    ## Time to normalize:
    ## for john in emission
    for word in emissions:
        ## for noun in emissions[john]
        for tag in emissions[word]:
            emissions[word][tag] = emissions[word][tag]/counts[tag]

    for tag in transitions:
        for tag_after in transitions[tag]:
            transitions[tag][tag_after] = transitions[tag][tag_after]/counts[tag]


    count_to_word = dict()
    test = open(test_file, "r")
    output = open(output_file, "w")
    # tags = list(transitions.keys())
    tags = ['NP0', 'VVD', 'AV0', 'PRP', 'AT0', 'NN1', 'PNP', 'VHG', 'VVN', 'VBD', 'AJ0', 'PUN', 'CJT', 'PNI', 'CJS', 'AJ0-VVG', 'PRF', 'VHD', 'DT0', 'NN1-VVB', 'VM0', 'VVI', 'CRD', 'NN2', 'AVP', 'PNQ', 'DPS', 'CJC', 'NN1-NP0', 'TO0', 'VVG', 'VVN-VVD', 'PRP-AVP', 'NN0', 'AJ0-VVD', 'PUQ', 'AVQ', 'VVZ', 'ORD', 'UNC', 'XX0', 'VVB-NN1', 'VVB', 'VHI', 'VBB', 'VBN', 'POS', 'AJ0-NN1', 'DTQ', 'PNX', 'AJS', 'VDN', 'AV0-AJ0', 'AJC', 'VBZ', 'VHB', 'VHZ', 'ITJ', 'VVD-VVN', 'CJS-PRP', 'VBI', 'NN1-AJ0', 'AVQ-CJS', 'VDB', 'VDZ', 'VDI', 'EX0', 'AJ0-AV0', 'VBG', 'VDD', 'ZZ0', 'CJS-AVQ', 'NN1-VVG', 'AVP-PRP', 'VVD-AJ0', 'VVN-AJ0', 'VVG-AJ0', 'AJ0-VVN', 'VVG-NN1', 'NP0-NN1', 'CJT-DT0', 'DT0-CJT', 'VDG', 'PRP-CJS', 'NN2-VVZ', 'VHN', 'PNI-CRD', 'VVZ-NN2', 'CRD-PNI', 'PUL', 'PUR']
    # print(len(tags))
    # print(tags)
    # tags.remove("sentence_start")
    previous_tag = "sentence_start"
    ## VITERBI
    for line in test:
        trellis = dict()
        word = line.strip()
        for tag in tags:
            if tag in transitions[previous_tag]:  
                transition = transitions[previous_tag][tag]
            else:
                transition = 0

            if (word in emissions) and (tag in emissions[word]):
                emission = emissions[word][tag]
            else:
                emission = 0
            
            prob = emission * transition
            trellis[tag] = prob
        # word_count += 1
        # if (word == "." or word == "?" or word =="!"):
        #     previous_tag = "sentence_start" 
        # arg max s/o to dictionaries
        best_tag = max(trellis, key=trellis.get)
        previous_tag = best_tag
        output.write(word + " : " + best_tag + "\n")

if __name__ == '__main__':
    # Run the tagger function.
    print("Starting the tagging process.")

    # Tagger expects the input call: "python3 tagger.py -d <training files> -t <test file> -o <output file>"
    parameters = sys.argv
    training_list = parameters[parameters.index("-d")+1:parameters.index("-t")]
    test_file = parameters[parameters.index("-t")+1]
    output_file = parameters[parameters.index("-o")+1]
    print(training_list)
    # print("Training files: " + str(training_list))
    # print("Test file: " + test_file)
    # print("Ouptut file: " + output_file)

    # Start the training and tagging operation.
    tag (training_list, test_file, output_file)