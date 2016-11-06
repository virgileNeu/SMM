# Swiss Music Map Project
> Project of the course Applied Data Analysis, by Michele Catasta
***
Virgile Neu, IN  
Alexandre Connat, SC  
Simon Narduzzi, IN

EPFL, November 2016

##Abstract
> Music is an art form and cultural activity whose medium is sound and silence, which exist in time. - Wikipedia  

Music is a way to express and share. It brings people together around a common focus. In ancient Greece, 
music is the most beautifl of the arts. Along with a science, it is the object of high philosophical speculation. The Greeks
are indeed the first people who have established real concerts, which contributed to the developpement of a socially 
conscious public actively participating in the hearing.

Through the ages, genres fall and rised, music has greatly evolved. However, the manner of celebrating and listening to music
 remained the same : the concerts.
 The goal of this project is to study the dynamics of music in Switzerland in recent decades, by studying the evolution of genres
 and number of auditors in concerts and major musical events.


##Data Description
###List of concert places

A first approach will be to use existing event websites to grab informations about the musical scene in Switzerland. We plan to get a list of all locations were we can attend a concert. Using the plateform Resident Advisor, we can a good list of clubs and concerts hall in Switzerland. The website contains all line-ups of the concerts that have been announced through RA since 2006, giving us approximately 10 years of data. As the plateform is mainly electronic music oriented, the data will be mostly related to Techno scenes and Electro clubs.

###Line-ups of Festivals / Concerts

We need to find several website of festival in Switzerland. We will build a dataset of all festival since 1980, and try to get the line-up for each of them. Of course, it will not be possible to get data for 36 years, as some festival just got created 10 or even 5 years ago. But we will try to get as much data as we can in order to perform analysis on genre and attendances of the festival. We will grab the line-up from official websites of festivals, and maybe other plateform, such as Facebook public events.

###Genres Analysis

Once we have the line-up of the concerts and festival, we can link the name of the artist to genre of music. There is a lot of genre possible, we need to select "main genres" that we can link to the data. We will perform a "merge" of subgenres, i.e : Hard Techno and Hardstyle = Electronic Music. If we have the time, we will try to divide our analysis in subgenre, but we will maybe not have enough data to have a viable statistical basis. The goal is to be able to detect rise and fall of music genre in Switzerland across the years.

We will mainly use a Wikipedia bot that will extract genre from artist name. The main challenge will be to try to get the genre of an artist if it does not have a Wikipedia biography.

###Artists Analysis

Using Wikipedia (and other biography pages), we can get the "profile" of an artiste. We can analyse its discography to observe genre change, and try to compare the popularity of an artist with the "trend" at that time in Swtizerland (hit parade, artist reputation).

Using the list of artist, we can also perform an analysis of the "foreign" rate of music : Do Switzerland always invited foreign musicians ? Do we observe a rise of local artists in big festivals ? What is the success of swiss artists abroad ?

##Feasability and Risks

##Deliverables

##Timeplan
