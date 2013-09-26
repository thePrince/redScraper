This is a project I am currently working on to get quantitative information about
how quickly reddit posts move up or down.  I call this velocity because the posts 
move with direction and magnitude.  The redReader script can be called on its own, 
but for data gathering purposes it is called through redComparer, which collects
various bits of data.  Currently only data on the top 25 posts is being colelcted;
since posts can only enter from one direction (rank 26+) this is easier to start with.

Velocity is currently being measured as the change in a post's ranking; the time at
which the script runs is also recorded for further analysis.  At this time I 
do not specifically keep track of which post is associated with a given velocity, though
it would be possible to extract that information from the output files.