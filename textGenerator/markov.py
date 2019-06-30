from numpy.random import randint


class MarkovChain:
    def __init__(self, user_id):
        """
        :param text: A list of the tweets for a given user
        """
        self.transition_dict = {}
        self.starting_words = []
        self.user_id = user_id

    def create_transition_dict(self, all_tweets):
        """
        Creates a dictionary where each key is the current state and the value is a
        list of the possible states that can be 'reached'.

        :param all_tweets: (List(String)) A list of all the tweets made by user_id
        """
        words = (" %$% ".join(all_tweets)).split(" ")  # Add separator to signify end of tweet
        self.starting_words = [string.split(" ", 1)[0] for string in all_tweets]

        index = 0
        while index <= len(words) - 2:
            current_word = words[index]
            next_word = words[index + 1]
            if current_word == "%$%" or current_word == "":
                index += 1
                continue
            elif next_word == "%$%" or next_word == "":
                index += 2
                continue

            if current_word in self.transition_dict.keys():
                self.transition_dict[current_word].append(next_word)
            else:
                self.transition_dict[current_word] = [next_word]

            index += 1

        for key, next_words in self.transition_dict.items():
            self.transition_dict[key] = list(filter(None, next_words))

    def generate_text(self, max_length):
        """
        Generates a snippet of text using the transition dictionary
        :param max_length: The desired length of the text
        :return: the generated text
        """
        tweet_ended = False  # True if text generation finished naturally (i.e. len < max_length)
        word_count = 1
        next_index = randint(0, len(self.starting_words))
        current_word = self.starting_words[next_index]
        text = current_word

        while word_count <= max_length and not tweet_ended:
            # Generates the next word based off of the current word
            if current_word in self.transition_dict.keys():
                next_states = self.transition_dict[current_word]
                next_index = randint(0, len(next_states))

                # "" terminate the text generation early and cannot be removed early on
                num_attempts = 0
                while next_states[next_index] == "" and num_attempts <= 10:
                    next_index = randint(0, len(next_states))
                    num_attempts += 1
                current_word = next_states[next_index]
                text += " " + current_word
            else:
                tweet_ended = True

            word_count += 1
        return text + "\n"

    def save_model(self):
        """
        Writes both the transition dictionary and starting words list to file
        :param user_id: The name of the user the transition dict is for.
        """
        with open(self.user_id + "_MC" + ".txt", 'w', encoding='utf-8') as file:
            # Writes in format: word:nextword,nextword,nextword,...
            for key, value in self.transition_dict.items():
                line = key + "~~~"
                for word in value:
                    line += word + ","
                file.write(line[:-1] + "\n")
            file.write("```\n")

            # Write the starting words to file
            for item in self.starting_words:
                file.write(item + "\n")

    def load_model(self):
        """
        Loads a pre-existing transition dictionary into this model.
        :param user_id: The name of the user for this transition dictionary.
        """
        starting_words = False
        with open(self.user_id + "_MC" + ".txt", encoding='utf-8') as file:
            for line in file.readlines():
                if line.strip() == "```":
                    starting_words = True

                if starting_words:
                    self.starting_words.append(line.strip())
                else:
                    line = line.strip().split("~~~")
                    next_words = line[1].split(",")
                    self.transition_dict[line[0]] = next_words
