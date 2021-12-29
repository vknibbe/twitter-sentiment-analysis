# Program to simplify manual labelling of tweets


def do_labelling():

    # open file containing unlabelled data, and file to write labelled data to
    with open('veg_full_tweets.txt', 'r', encoding='utf-8') as file, open('veg_full_labelled.txt', 'a', encoding='utf-8') as label_file:

        # read in unlabelled data
        full_tweets=file.readlines()

        # loop through the tweets
        for tweet in full_tweets:
            labelled = False
            tweet = tweet.strip()

            # split the line of tweet data, to be able to access tweet text
            tweet_list = tweet.split(';')

            try:
                while not labelled:

                    print(tweet_list[0])
                    label = input("Please select: f=positive, j=negative, space=neutral")

                    # if positive selected, append positive label and flag tweet as labelled
                    if label == 'f':
                        label_file.write(tweet + ';positive\n')
                        labelled = True

                    # if negative selected, append negative label and flag tweet as labelled
                    elif label == 'j':
                        label_file.write(tweet + ';negative\n')
                        labelled = True

                    # if neutral selected, append neutral label and flag tweet as labelled
                    elif label == ' ':
                        label_file.write(tweet + ';neutral\n')
                        labelled = True

                    # if any other key selected, discard tweet (just in case)
                    else:
                        raise Exception('exited')
            except:
                continue

        print("well done, labelling finished")



# run labelling function
do_labelling()