# to take in a csv file and show voting results of a hare-clark model

#input how many seats available
while True:
    try:
        seats = int(input("How many seats are available? "))
        break
    except:
        print("Answer as an integer only")

filled_seats = []
lost = []
print("total seats = " + str(seats));

#read the voting results from csv file
import csv;
ballots = [];

#for each ballot, adding upto attribute and value attribute and log
with open("./votes.csv","r") as file:
    csvreader = csv.reader(file);
    for row in csvreader:
        ballots.append([row,1,1,""]);

#creating starting conditions
remain = []
candidates = ballots[0][0];
cand_count =len(candidates);
print("Number of Candidates: "+str(cand_count));
for x in range(cand_count):
    remain.append(x)
ballots.pop(0);
#print(candidates);
#print(ballots);
assigned_ballots = []
for candidate in candidates:
    assigned_ballots.append([])
#print(assigned_ballots); #should be blank 2d array with appropriate number of slots

#gather number of votes
t_ballots = len(ballots);
print("total ballots = " + str(t_ballots));

#calculate the quota (total ballots / (vacancies + 1))+1
quota = (t_ballots/(seats + 1))+1
print("quota = " + str(quota))

#initial assign ballots to candidates
for paper in ballots:
    #check where current upto is ticked
    i = 0
    for column in paper[0]:
        if int(column) == paper[1]:
            paper[3] = paper[3] + str("Ballot assigned to "+candidates[i]+". ");
            assigned_ballots[i].append(paper);        
        i = i + 1;

keepcounting = True
round = 1
while keepcounting:

    print()
    print("Round "+str(round))

    #reassign filled_seat ballots
    for cand in filled_seats:
        #calulating votes and new values to assign to ballots
        votes = 0
        ballots_to_reassign = len(assigned_ballots[cand]);
        if  ballots_to_reassign !=0:
            #print("to reassign: "+str(ballots_to_reassign));
            for paper in assigned_ballots[cand]:      
                votes= votes + paper[2]; #adding value of the ballot
            new_value = (votes - quota) / votes; #calulating transfer value
            #print("transfer value: "+str(new_value));

            for paper in assigned_ballots[cand]:
                i = 0;
                to_assess = True;
                paper[2]=new_value;
                while to_assess:
                    paper[1]=paper[1]+1;
                    for column in paper[0]:
                        if int(column) == paper[1]:
                            if (i in filled_seats) or (i in lost):
                                paper[1]=paper[1]+1;
                            else:
                                paper[3] = paper[3] + str("Ballot assigned to "+candidates[i]+". ");
                                assigned_ballots[i].append(paper);
                                to_assess = False;
                        if i == (cand_count-1):
                            i=0;
                        else:
                            i=i+1;
            assigned_ballots[cand] = []; #clear assigned ballots
    
    #reassign lost ballots
    for cand in lost:
        #calulating votes and new values to assign to ballots
        votes = 0
        ballots_to_reassign = len(assigned_ballots[cand]);
        if  ballots_to_reassign !=0:
            #print("to reassign: "+str(ballots_to_reassign));
            #print("transfering remaining value");
            for paper in assigned_ballots[cand]:
                i = 0;
                to_assess = True;
                while to_assess:
                    for column in paper[0]:
                        if int(column) == paper[1]:
                            if (i in filled_seats) or (i in lost):
                                paper[1]=paper[1]+1;
                            else:
                                paper[3] = paper[3] + str("Ballot assigned to "+candidates[i]+". ");
                                assigned_ballots[i].append(paper);
                                to_assess = False;
                        if i == (cand_count-1):
                            i=0;
                        else:
                            i=i+1;
            assigned_ballots[cand] = []; #clear assigned ballots


    #print(assigned_ballots)
    #results of round
    print("Results:")
    print("quota = " + str(quota))
    i = 0;
    lowest_votes = quota;
    chopping_block = [];
    noone_quota= True;
    for row in assigned_ballots:
        votes = 0
        if i in remain:
            for paper in row:
                votes= votes + paper[2]; #adding value of the ballot
            print(candidates[i]+": "+str(votes))

            if votes >= quota:
                noone_quota=False;
                filled_seats.append(i);
                remain.remove(i);
            if votes < lowest_votes:
                lowest_votes = votes;
                chopping_block= [i];
            elif votes == lowest_votes:
                chopping_block.append(i);        
        i = i+1;

    #checks if there are candidates left for seats
    if len(remain) <= seats-len(filled_seats):        
        for x in remain:
            filled_seats.append(x);
        remain = []
        keepcounting = False;
    #if noone reached quota and competition left, lowest eliminated
    elif noone_quota:
        for x in chopping_block:
            lost.append(x);
            remain.remove(x);


    print("Filled Seats: "+str(len(filled_seats)));
    print("Candidates Eliminated: "+str(len(lost)));
    print("Candidates Remaining: "+str(len(remain)));
    print("Seats remaining: "+str(seats-len(filled_seats)));

    if seats-len(filled_seats) <= 0:
        keepcounting = False;
         
    round = round + 1;

print("")
print("The winners are:")
for cand in filled_seats:
    print(candidates[cand]);
