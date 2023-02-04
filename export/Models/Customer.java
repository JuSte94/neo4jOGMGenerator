package com.example.demo;

    import org.neo4j.ogm.annotation.NodeEntity;
import org.neo4j.ogm.annotation.Id;
import org.neo4j.ogm.annotation.Labels;
import lombok.Getter;
import lombok.Setter;
    public  class Customer extends User {
        

        @Relationship(type="HAT_STATUS", direction="OUTGOING")
		private Status Status
    }
    