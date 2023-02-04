package com.example.demo;

    import org.neo4j.ogm.annotation.NodeEntity;
import org.neo4j.ogm.annotation.Id;
import org.neo4j.ogm.annotation.Labels;
import lombok.Getter;
import lombok.Setter;
    public  class Trainigsplan  {
        private String status;
private String name;
private String beschreibung;
@Id
private String Id;


        @Relationship(type="HAT_STATUS", direction="OUTGOING")
		private Status Status
    }
    