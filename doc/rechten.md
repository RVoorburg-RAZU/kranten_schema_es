# Metadata auteursrecht & licenties voor periodieken 

## Inleiding

In de e-depot-metadata geven we via de de relatie `ldto:beperkingGebruik` o.a. aan welke beperkingen relevant zijn die te maken hebben met auteursrecht, waaronder ook gebruikslicenties. De relatie verwijst naar een blanknode (node zonder URI) van het type `ldto:BeperkingGebruikGegevens`. De belangrijkste relatie daarbinnen is `ldto:beperkingGebruikType`. Dit verwijst naar concepten in de thesaurus. Mogelijke concepten zijn bijvoorbeeld "Onder auteursrecht", of een licentie als CC-0.

Het doel van de metadata is niet om volledig de auteursrechtelijke situatie vast te leggen maar enkel alleen om aan te geven welke confities of het gebruik van de objecten beperken. Zo leggen niet expliciet vast dat een stuk onder auteurrecht valt als er ook een licentie is die binnen dat wettelijk kader de gebruiksmogelijkheden verruimt. In dat geval leggen we de licentie vast.

Optioneel kunnen we in de metadata met `ldto:beperkingGebruikTermijn` aangeven tot wanneer een specifieke beperking (een specifiek `ldto:beperkingGebruikType`) speelt. 


## Mogelijke situaties

### Auteursrechtelijk beschermd zonder licentie of overeenkomst
Auteursrechtelijk beschermd zonder licentie of overeenkomst  - **beperkt openbaar**

    [
        a ldto:BeperkingGebruikGegevens ;
        ldto:beperkingGebruikType <https://data.razu.nl/id/beperkinggebruiktype/3e82de530014486e637ea9257088ccea> ; # Auteursrecht
    ]

### Auteursrechtelijk beschermd met licentie met de uitgever, ouder dan 10 jaar
Auteursrechtelijk beschermd maar we hebben een licentie met de uitgever EN ouder dan 10 jaar - **openbaar** onder voorwaarden van die licentie, plus de koepelovereenkomst

    [
        a ldto:BeperkingGebruikGegevens ;
        ldto:beperkingGebruikType <https://data.razu.nl/id/beperkinggebruiktype/0ee107032f9027f2d9c6ba381b881f29> ; # vb: naamsvermelding + NC
    ], [ 
        a ldto:BeperkingGebruikGegevens ;
        ldto:beperkingGebruikType <https://data.razu.nl/id/beperkinggebruiktype/b270c98d99c3e7951da85ca84a34f35a> ; # koepelovereenkomst.
    ]

### Auteursrechtelijk beschermd zonder licentie met de uitgever, ouder dan 10 jaar 

Auteursrechtelijk beschermd zonder licentie met de uitgever (want we weten niet wie de uitgeversrechten heeft) EN ouder dan 10 jaar - **openbaar** onder voorwaarden van de koepelovereenkomst. Hier nemen we een risico op het gebied van de auteursrechten van de uitgever. We zouden een notitie kunnen opnemen in de e-depot-metadata, of hier verwijzen in naar een notitie, of de notitie alleen in interne systemen vastleggen. Voorbeeld geeft een uitwerking van optie 1. 

    [ 
        a ldto:BeperkingGebruikGegevens ;
        ldto:beperkingGebruikType <https://data.razu.nl/id/beperkinggebruiktype/b270c98d99c3e7951da85ca84a34f35a> ; # koepelovereenkomst
        ldto:beperkingGebruikNadereBeschrijving "onduidelijk waar uitgeversrechten liggen"
    ] 


### Auteursrechtelijk beschermd met licentie met de uitgever, jonger dan 10 jaar

Auteursrechtelijk beschermd maar we hebben een licentie met de uitgever EN jonger dan 10 jaar - **beperkt openbaar** onder de voorwaarden van de koepelovereenkomst. Voorstel is om dit als volgt in de metadata vast te leggen:

    [
        a ldto:BeperkingGebruikGegevens ;
        ldto:beperkingGebruikType <https://data.razu.nl/id/beperkinggebruiktype/3e82de530014486e637ea9257088ccea> ; # auteursrecht
        ldto:beperkingGebruikTermijn [
            a ldto:TermijnGegevens ;
            ldto:termijnEinddatum "2026-06-16"^^xsd:date
        ]
    ], [
        a ldto:BeperkingGebruikGegevens ;
        ldto:beperkingGebruikType <https://data.razu.nl/id/beperkinggebruiktype/0ee107032f9027f2d9c6ba381b881f29> ; # vb: naamsvermelding + NC
    ], [ 
        a ldto:BeperkingGebruikGegevens ;
        ldto:beperkingGebruikType <https://data.razu.nl/id/beperkinggebruiktype/b270c98d99c3e7951da85ca84a34f35a> ; # koepelovereenkomst.
    ]

Bemerk dat `ldto:termijnEinddatum "2026-06-16"^^xsd:date` niet betekent dat na die datum het stuk vrij is van auteursrecht. Het geeft aan dat auteurswettelijke beperkingen na die datum niet direct van invloed zijn omdat licenties de aard van de toegang bepalen.

### Auteursrechtelijk beschermd zonder licentie met de uitgever, jonger dan 10 jaar
Auteursrechtelijk beschermd zonder licentie met de uitgever (want we weten niet wie de uitgeversrechten heeft) EN jonger dan 10 jaar - **beperkt openbaar** onder de voorwaarden van de koepelovereenkomst

    [
        a ldto:BeperkingGebruikGegevens ;
        ldto:beperkingGebruikType <https://data.razu.nl/id/beperkinggebruiktype/3e82de530014486e637ea9257088ccea> ; # auteursrecht
        ldto:beperkingGebruikTermijn [
            a ldto:TermijnGegevens ;
            ldto:termijnEinddatum "2026-06-16"^^xsd:date
        ]
    ], [ 
        a ldto:BeperkingGebruikGegevens ;
        ldto:beperkingGebruikType <https://data.razu.nl/id/beperkinggebruiktype/b270c98d99c3e7951da85ca84a34f35a> ; # koepelovereenkomst
        ldto:beperkingGebruikNadereBeschrijving "onduidelijk waar uitgeversrechten liggen"
    ] 


### Ouder dan 70 jaar, maar jonger dan 150 jaar
Ouder dan 70 jaar, maar jonger dan 150 jaar - **openbaar** onder voorwaarden van de koepelovereenkomst

    [ 
        a ldto:BeperkingGebruikGegevens ;
        ldto:beperkingGebruikType <https://data.razu.nl/id/beperkinggebruiktype/b270c98d99c3e7951da85ca84a34f35a> ; # koepelovereenkomst.
    ]


### Ouder dan 150 jaar
Ouder dan 150 jaar - openbaar zonder voorwaarden

    [ 
        a ldto:BeperkingGebruikGegevens ;
        ldto:beperkingGebruikType <https://data.razu.nl/id/beperkinggebruiktype/2a747f5ab4430d474995c8fcd877c7ef> ; # public domain.
    ]


## Samenvattend

Als onbekend is wie de uitgever is maar het materiaal valt wel onder de koepelovereenkomst, dan **openbaar**. Ookal weten wij niet welke freelancers in die bladen gepubliceerd hebben. Dat vangt de koepelovk voor ons af met de opt-out optie. 
Als we NIET weten wie de uitgever is en het materiaal valt ook niet onder de koepelovereenkomst (jonger dan 10 jaar) dan **beperkt openbaar**. In de metadata is al het materiaal in deze categorie te herkennen aan `ldto:beperkingGebruikGegevens` met een `ldto:beperkingGebruikType` "onder auteursrecht" , mits de daarbij vermelde termijn niet verstreken is.
