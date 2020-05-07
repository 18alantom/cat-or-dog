import numpy as np
import json

cat = [
    ["That's definitely a cat.", "Cat for sure.",
        "That's a cat, I know it in my neurons!", "CAT!!"],
    ["I'm like 90 percent sure that's a cat",
     "I think it's a cat", "cat... right?", "Hmmm, cat?"],
    ["🧐looks kinda like a cat", "Probably a cat..",
     "Very cat like, but is it?", "I don't know, might be a cat."],
    ["??", "What's that", "Definitely a person?",
     "Correct me if I'm wrong but that isn't a dog."]
]
dog = [
    ["DOGGIE!!", "I'm like 90 percent sure that's a dog",
        "An AI's best friend? A dog!", "Dog for sure!"],
    ["Mostly a dog.", "A dog but could be a wolf too.",
     "Well it looks like a dog?!", "If it barks it's a dog"],
    ["That's a dog?", "Hmmm... dog?",
     "Like 80 percent sure that's a dog", "That.. is a dog? 🤨"],
    ["Is that like an otter or something?", "A wall!",
     "You have confounded my neurons dear person, I cede!", "Not a cat?"]
]


def prob_to_index(prob):
    if prob > 0.98:
        return 0
    elif prob > 0.9:
        return 1
    elif prob > 0.8:
        return 2
    else:
        return 3


def what_is_it(cat_prob, dog_prob):
    is_cat = cat_prob > dog_prob
    prob = cat_prob if is_cat else dog_prob

    verdict = ""
    arr = dog

    if is_cat:
        arr = cat

    i = prob_to_index(prob)
    l = len(arr[i])
    verdict = arr[i][np.random.randint(0, l)]

    response = json.dumps(
        {"verdict": verdict, "probability": cat_prob.item()})
    return response
