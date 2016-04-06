#Hillary's Inbox: A text analysis of (a subset of) emails sent and received by Hillary Clinton on her private server

###Project Update

1) Did you meet your first milestone?

Yes - I have completed basic n-gram classification and topic analysis. I
extracted the relevant data I was looking for (email body text) and classified
the text into several groups, on which I then ran gensim's lda model. I
narrowed down on the question of figuring out how interactions differed between
different groups of people in Hillary's network - friends versus professionals,
specifically. In addition, I decided to group together the text into emails
sent by females and males just out of interest. Notably, my dataset right now only includes 
emails sent to Hillary Clinton, not sent by her. This is due to noticing some gaps in
my dataset that I hope to fill or find out why they're not present.

In addition, I've decided to run sentiment analysis on the email corpus to see
if the tone of emails is correlated to the sender of the email, but I'm still
working on finding a suitible training set for the analysis.

2) What have you finished so far?

See above - I've finished topic modeling and n-gram analysis. The results are
interesting, although I'm not sure that they're telling of a broader story. For
example, there are topics that consist of the words [bloomberg, commentary
opinion] and [bloomberg, mr., company, state] among the corpus of emails with
Hillary's friends. Clearly, there must have been a controversial article that
her friends felt compelled to send to her.

I also found that a lot of the emails dealt with logistics. For example, when I
run the topic analysis on the entire corpus of emails, there's a topic
containing the words [office, secretary, room, meeting, arrive] which I assume
are sent by her assistants.

As mentioned previously, I also ran an n-gram analysis on each subset of the
email corpus. I found that there wasn't a large varience in terms of word
length, sentence length, or number of words used among males and females. Her
staffers send slightly shorter emails (shorter in average sentence length by
one word) compared to people who don't work in her office.

3) Are your results satisfactory?

Yes and no. Yes in that I was able to extract meaningful topics from the email
corpus. No in that I don't think it's particularly insightful that Hillary
talked about Benghazi, for example, without further context of what she said. I
think my results will be more satisfactory if I'm able to successfully narrow
down a few groups that give distinct topic results. I also think after I run
the sentiment analysis that I'll have more to work with.

4) Updates to project plan

As mentioned, I'm planning on running sentiment analysis. In addition to topic
analysis, I think that running a k-clustering algorithm on the corpus could be
telling to discover clusters of topics that might not have been picked up by
the LDA analysis.

5) Difficulties and questions

I'm not too sure where to get a suitible training set for sentiment analysis
without tagging lots of words / sentences myself. Because Hillary's topics tend
to be very specific in temrs of foreign policy, my concern is that there isn't
going to be meaningful training data. 
 
