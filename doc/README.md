Ontwerp krantenmetadata in LDTO

Deze repository biedt een ontwerp voor een toepassingsprofiel of uibreiding van LDTO-metadata voor het opnemen van krantenmetadata.

Uitgangspunten zijn:
- LDTO biedt het kader voor het bewaren en beheren krantenmetadata als archief
- Voor een bibliografisch perspectief breiden we LDTO uit met schema.org-metadata.


LDTO als kader vraag om de opzet van een hiérarchie van ldto:Informatieobjecten. Zeker deze niveaus zijn dan wenselijk:
1. De collectie van alle kranten.
2. De verzameling van kranten die tot één titel behoren.
3. Een aflevering ( issue') van een krant.

Het niveau van de collectie zouden we dan als volgt kunnen invullen:

<collectie>                                                 # de URI van deze collectie, nu een fictieve waarde
    a ldto:Informatieobject ;
    ldto:aggregatieniveau "archief" ;                       # "archief" is het hoogste niveau in de ldto:Informatieobjecten-hiërarchie
    ldto:classificatie "bibliografische collectie" ;        # ter aanvulling classificeren we dit als een 'bibliografische collectie'
    ldto:naam "RAZU Krantencollectie" ;                     # we geven een naam
    ldto:archiefvormer <https://data.razu.nl/id/actor/2bdb658a032a405d71c19159bd2bbb3a> ;  # = "RAZU", deze collectie is opgebouwd door RAZU 
    ldto:dekkingInTijd [ a ldto:DekkingInTijdGegevens ;                                    #  de datumrange van al kranten in deze collectie
        ldto:dekkingInTijdBeginDatum "1800"^^xsd:gYear ; 
        ldto:dekkingInTijdEindDatum "1980"^^xsd:gYear ;  
        ldto:dekkingInTijdType <https://data.razu.nl/id/dekkingintijdtype/a3e30182626730af3b3c2a7071c58038> # = Verschijningsperiode 
    ] ;
    dct:hasFormat <https://k50907905.opslag.razu.nl/NL-WbDRAZU-K50907905-collectie.meta.json> .             # de URI van deze metadata zelf 

Let op, ldto:aggregatieniveau en ldto:classificatie krigen als waarde een URI, hier voor de leesbaarheid als een literal getoond.
Omdat hier gekozen is RAZU als archiefvormer te zien (wat nadrukkelijk wat anders is dan bijvoorbeeld de uitgever van een krant), wordt dit archief ook bewaard in de S3-bucket van RAZU.
In het voorbeeld is niet expliciet een ldto:identifier opgenomen. Hier is de URI, het subject, de identifier. Een ldto:identifier kan opgegeven worden om bijvoorbeeld een koppeling met deze collectie in een legacy-systeem vast te leggen.
We linken altijd van lager in de hiërarchie naar hoger in de hiërarchie. Op het hoogste niveau zijn er dus geen links naar een lager niveau.

Het niveau van de verzameling van kranten met dezelfde titel is een ldto:Informatieobject op het ldto:aggregatieniveau "serie". Deze "serie" is niet één-op-één gelijk aan een krantentitel. De "serie" is een concrete verzameling van archiefstukken, een (kranten-) titel is een abstractere identiteit. Gesteld kan worden dat het ldto:Informatieobject betrekking heeft op de krantentitel (als groepering-criterium). Dit onderscheid leggen we als volgt vast":

<serie>                                                     # de URI van een titel-serie, nu een fictieve waarde
    a ldto:Informatieobject ;
    ldto:aggregatieniveau "serie";                          
    ldto:classificatie "krantentitel" ;                    # niet te lezen als een isA-relatie, geeft wel indicatie inhoud
    ldto:naam "De Amerongse Courant" ;                     # naam van betreffende krant
    ldto:archiefvormer <https://data.razu.nl/id/actor/2bdb658a032a405d71c19159bd2bbb3a> ;               # = "RAZU 
    ldto:isOnderdeelVan <collectie> ;
    ldto:dekkingInTijd [ a ldto:DekkingInTijdGegevens ;             # geeft aan welke wat we hebben in deze serie,     
        ldto:dekkingInTijdBeginDatum "1878"^^xsd:gYear ;            # niet wanneer de titel is uitgegeven
        ldto:dekkingInTijdEindDatum "1929"^^xsd:gYear ;
        ldto:dekkingInTijdType <https://data.razu.nl/id/dekkingintijdtype/a3e30182626730af3b3c2a7071c58038> # = Verschijningsperiode 
    ] , [
        ldto:dekkingInTijdBeginDatum "1941"^^xsd:gYear ; 
        ldto:dekkingInTijdEindDatum "1941"^^xsd:gYear ;  
        ldto:dekkingInTijdType <https://data.razu.nl/id/dekkingintijdtype/a3e30182626730af3b3c2a7071c58038> # = Verschijningsperiode 
    ] ;
    ldto:beperkingGebruik <https://data.razu.nl/id/licentie/c9ff6ea52d650cc82c5c04dd054aeb1f> ;
    ldto:dekkingInRuimte "Amerongen", "Leersum", "Maarn", "Maarsbergen", "Doorn", "Driebergen", "Langbroek", "Cothen", "Wijk bij Duurstede" ;  # maar dan uris
    schema:mainEntity [
        # dit *is* de krantentitel in bibliografische zin:
        a schema:Newspaper ; 
        schema:name "De Amerongse Courant" ;
        schema:alternateName "Nieuws- en advertentieblad voor Amerongen, Leersum, Maarn, Maarsbergen, Doorn, Driebergen, Langbroek, Cothen, Wijk-bij-Duurstede enz" ;
        schema:spatialCoverage "Amerongen", "Leersum", "Maarn", "Maarsbergen", "Doorn", "Driebergen", "Langbroek", "Cothen", "Wijk bij Duurstede" ; 
        schema:temporalCoverage "1870-" ;              # format??? ; geeft hier aan wanneer uitgekomen, dus niet per se gelijk aan de ldto:dekkingInTijd
        schema:publisher "B. Ruitenbeek - Doorn" ;               # wordt een URI uit onze actoren-thesaurus
        schema:sameAs <EXTERNE URIs, KB catalogus e.d> 
    ] ;
    dct:hasFormat <https://k50907905.opslag.razu.nl/NL-WbDRAZU-K50907905-serie.meta.json> .             # de URI van deze metadata zelf 

Het koppeling tussen de serie van archiefstukken die tot de zelfde titel behoren als de titel zelf, gebeurt hier via de schema:mainEntity-relatie. Bemerk dat de dekkingInTijd / temporalCoverage kunnen verschillen.

Één niveau lager is het ldto:Informatieobject het gearchiveerde exemplaar van een aflevering van het tijdschrift. Ook hier wordt de relatie tussen het concrete archiefstuk de abstractere aflevering gerepresenteerd via de schema:mainEntity-relatie:

<aflevering>
    a ldto:Informatieobject ;
    ldto:aggregatieniveau "archiefstuk";                                                    # issue is een archiefstuk?  we bewaren issues dus ja,     
    ldto:classificatie "aflevering krant" ;                                                 # niet te lezen als een isA-relatie, geeft wel indicatie inhoud
    ldto:naam "De Amerongse Courant, 28 december 1929" ;                                    #  hoe willen we dit formatteren? issue nr er bij?
    ldto:archiefvormer <https://data.razu.nl/id/actor/2bdb658a032a405d71c19159bd2bbb3a> ;   # = RAZU 
    ldto:isOnderdeelVan <serie> ;
    ldto:locatie "hier aangeven waar dit archiefstuk in depot te vinden is" ;               # hoe gaan we dit precies formatteren?
    ldto:dekkingInTijd [ a ldto:DekkingInTijdGegevens ;     
        ldto:dekkingInTijdBeginDatum "1929-12-28"^^xsd:date  ; 
        ldto:dekkingInTijdEindDatum "1929-12-28"^^xsd:date ;  
        ldto:dekkingInTijdType <https://data.razu.nl/id/dekkingintijdtype/a3e30182626730af3c2a7071c58038> # = Verschijningsperiode 
    ] ;
    ldto:beperkingGebruik <https://data.razu.nl/id/licentie/c9ff6ea52d650cc82c5c04dd054aeb1f> ;
    ldto:dekkingInRuimte "Amerongen", "Leersum", "Maarn", "Maarsbergen", "Doorn", "Driebergen", "Langbroek", "Cothen", "Wijk bij Duurstede" ;  # maar dan uris
    schema:mainEntity [  
        a schema:PublicationIssue ;
        schema:name "De Amerongse Courant, 28 december 1929" ;
        schema:alternateName "Nieuws- en advertentieblad voor Amerongen, Leersum, Maarn, Maarsbergen, Doorn, Driebergen, Langbroek, Cothen, Wijk-bij-Duurstede enz" ;
        schema:datePublished "1929-12-28"^^xsd:date ;
        schema:isPartOf [
            a schema:PublicationVolume  ;
            schema:volumeNumber "8" 
        ] ;
        schema:issueNumber "52"
    ] ;
    dct:hasFormat <https://k50907905.opslag.razu.nl/NL-WbDRAZU-K50907905-aflevering.meta.json> .             # de URI van deze metadata zelf 


Van een aflevering worden digitaal, als bestand, de pagina's bewaard. Om de metadata eenvoudig te houden, en de verwarring te voorkomen dat een archiefstuk ook weer archiefstukken bevat, modeleren we een pagina niet als een ldto:Informatieobject maar enkel als een ldto:Bestand dat een representatie biedt van de aflevering. Op pagina-niveau zijn meerdere represenaties mogelijk, bijvoorbeeld de afbeelding (scan) of de alto-xml.

<pagina_1>
    a ldto:Bestand ;
    ldto:naam "Pagina 1, De Amerongse Courant, 28 december 1929" ;                      # of we houden het hier heel kort, nemen het wel uitgebreider op in Elastic Seacr  
    ldto:URLBestand "https://k50907905.opslag.razu.nl/NL-WbDRAZU-K50907905-500-999.jp2"^^xsd:anyURI ;
    ldto:bestandsformaat <https://data.razu.nl/id/bestandsformaat/84621bf26697a4a776a9007b97023412> ;  # jp2
    ldto:checksum [ a ldto:ChecksumGegevens ;
        ldto:checksumAlgoritme <https://data.razu.nl/id/algoritme/7f138a09169b250e9dcb378140907378> ;
        ldto:checksumDatum "2025-01-13T10:28:59.004406+00:00"^^xsd:dateTime ;
        ldto:checksumWaarde "c2c90c72aa8516a171324793cba37407" ] ;
    ldto:isRepresentatieVan <aflevering> ;
    ldto:omvang 370539 ;
    schema:width 4000 ;
    schema:height 6000 ;
    schema:position 1;
    iiif:service <https://iiif.example.com/iiif/issue1/page1> ;
    dct:hasFormat <https://k50907905.opslag.razu.nl/NL-WbDRAZU-K50907905-pagina_1.meta.json> . 

Bovenstaande geeft de afbeelding van pagina 1. Het is herkenbaar als afbeelding door het ldto:bestandsformaat en dat een breedte en een hoogte gegeven zijn. In aanvulling op de URI van het object, de locatie op de S3 (ldto:URLBestand) en locatie van deze metadata op de S3 (dct:hasFormat) biedt deze metadata ook de IIIF-URI van de afbeelding zoals beschikbaar via de (nog in te richten IIIF-service).

Als het bestand representatief zou zijn voor het volledige exemplaar van de aflevering dan zou attribuut 'schema:position' ontbreken.
Als het bestand een alto-xml zou zijn dan zou dat indirect herleid kunnen worden aan het ldto:bestandsformaat ("xml") en aan de extensie in ldto:URLBestand (eingdigt op "alto.xml"). Daarnaast zou het object geen attributen schema:width, schema:height of iiif.service bevatten.








Het is denkbaar dat er ook representaties zijn van de aflevering die niet betrekking hebben op een pagina maar op het gehele exemplaar. Di







