Notes from Brady:
  player.sql is just the sql file on Sprint 2 (and also on the helper github I think)
  python-pg seemed to be the sql database we are supposed to work with so I just built on top of that
  the python-pg lets you enter an id into the database, and then does the check to see if it exists and stuff


Notes from Matthew:
  Initial UDP client and server set up for sending codes, just need integration with Database and Player Entry Screen
  TODO: Integrate UDP functionality into the Player Entry Screen 
    -When a player is added, call the UDP client's function to send that player's equipment code
  TODO: Database integration
    -After inserting a player into the Database, have a UDP message directly from database or as part of player entry logic
    
  I will go in and do these TODOs in the database/Player Entry Screen, I just put this here so everyone knows where the UDP part is at.
  
