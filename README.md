# Wordle-game

## Introduction

This is a client program that plays a variant of the recently-popular game Wordle. The server was provided during the course Networks & Distributed Systems at Northeastern University. The program makes guesses for the secret word, and the server gives information about how close each guess is. Once the client correctly guesses the word, the server returns a secret flag.

## Algorithm

My high-level approach consists of a search algorithm with some criteria applied to reduce the number of possible guesses. We can describe the algorithm as follows:

1) My first guess is the first word on the list of possible answers.

2) Then I analyze the mark obtained, to update 3 data structures that I use to find the next possible candidate: 
    2.1) wrong_letters: It's a set that contains all the letters that have obtained a 0 mark, except those who had also obtained a 2 mark in the same word. 
    2.2) right_letters: It's a set that contains all the letters that have obtained a 1 or 2 mark.
    2.3) word_guess: It's a list of 5 strings in which I indicate the letters with a 2 mark, in the corresponding position.

3) Then, I use the previous structures to choose my next guess. I just iterate one by one looking for a word that:
    3.1) Has no wrong letters
    3.2) Has all the right letters
    3.3) Has all the letters of my word_guess in the corresponding position

4) Finally, we iterate the 2) and 3) steps until we find the correct word.

I want to emphasize the importance of choosing the correct data structures, depending on the task that are going to be used.
 - I'm using sets when I need a structure with no repeated elements, that allows me to add and search elements efficiently (O(1)).
 - I'm using lists when I need to access the elements by index (O(1)).
 - I'm using dictionaries when I want to access an element by a key (O(1))
This is not crucial in this case because the n is not that big, but it would be very important if we want to generalize.
