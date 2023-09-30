CREATE TABLE agents {
    agent_name varchar(15),
    agent_function varchar(15),
    ability1_name varchar(20),
    ability1_description varchar(500),
    ability2_name varchar(20),
    ability2_description varchar(500),
    ability3_name varchar(20),
    ability3_description varchar(500),
    ultimate_name varchar(20),
    ultimate_description varchar(500)  
};

CREATE TABLE maps {
    map_name varchar(20),
};

CREATE TABLE users {
    id serial PRIMARY KEY,
    username varchar(50) not null,
    password varchar(100) not null,
    email varchar(30) unique not null
};
