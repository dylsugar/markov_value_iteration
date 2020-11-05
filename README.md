Write Up:

The zipfile given includes mdp_input.txt, mdp_input_book.txt, and mdp.py

  Running Program:
  1) In command line, type :      python3 mdp.py <name of txt file>
  2) Output should show all iterations and the final policy at the bottom
  
  Input .txt file format:
  - my code is specific where I parse each line based on the length of the word, so if the wording on the input file doesn't match the one from the sample, then there might be an error, however, I tested all the samples and they work just fine. 
  - each line is separated by a "#" comment, but I parse looking for "size :", "walls :","terminal_states :", "reward :", etc
  - the data from each line is stored in my Grid class
