# Ontwerp krantenmetadata in LDTO

Deze repository biedt een ontwerp voor een toepassingsprofiel of uibreiding van LDTO-metadata voor het opnemen van krantenmetadata.

Uitgangspunten zijn:
- LDTO biedt het kader voor het bewaren en beheren krantenmetadata als beschrijving van *archief*
- Voor een *bibliografisch perspectief* breiden we LDTO uit met schema.org-metadata.


LDTO als kader vraag om de opzet van een hiërarchie van `ldto:Informatieobjecten`. Zeker deze niveaus zijn dan wenselijk:
1. De collectie van alle kranten,
2. De verzameling van kranten die tot één titel behoren,
3. Een exemplaar van een een aflevering ( issue') van een krant.

## Collectie
Het niveau van de collectie zouden we dan als volgt kunnen invullen:

    <https://data.razu.nl/id/object/NL-WbDRAZU-K50907905-1234-0>
        a ldto:Informatieobject ;
        ldto:aggregatieniveau <https://data.razu.nl/id/aggregatieniveau/62d05f1b8d586edb7da7f257be926705> ;  # archief
        ldto:classificatie <https://data.razu.nl/id/soort89cfa9e6349cc6bdf87135c96cd37e14>  ;   # bibliografische collectie
        ldto:naam "Collectie kranten" ;                                                         # model "Collectie xxx" - beginkapitaal? 
        ldto:archiefvormer <https://data.razu.nl/id/actor/2bdb658a032a405d71c19159bd2bbb3a>,    # RAZU 
            <https://data.razu.nl/id/actor/aafc151236a6978fdf1732dcadb53f2e> ;                  # Utrechtse Heuvelrug (etc.)
        ldto:dekkingInTijd [ 
            a ldto:DekkingInTijdGegevens ;                                                      # de datumrange van al kranten in deze collectie
            ldto:dekkingInTijdBeginDatum "1800"^^xsd:gYear ;                                    # altijd ISO 8601, maar ranges opgesplitst
            ldto:dekkingInTijdEindDatum "1980"^^xsd:gYear ;  
            ldto:dekkingInTijdType <https://data.razu.nl/id/dekkingintijdtype/a3e30182626730af3b3c2a7071c58038> # = Verschijningsperiode 
        ] ;
        dct:hasFormat <https://k50907905.opslag.razu.nl/NL-WbDRAZU-K50907905-1234-0.meta.json>. # locatie van deze metadata op de storage  
 
Deze collectie omsluit materiaal van meerdere archiefvormers. Het materiaal wordt bewaard in de S3-bucket op naam van RAZU (inclusief bijbehordende naamgeving URIs). In het voorbeeld is niet expliciet een `ldto:identifier` opgenomen. Hier is de URI, het RDF-subject, de identifier. Een `ldto:identifier` kan opgegeven worden om bijvoorbeeld een koppeling met deze collectie in een legacy-systeem vast te leggen. We linken altijd van lager in de hiërarchie naar hoger in de hiërarchie. Op dit hoogste niveau zijn er dus geen links naar een lager niveau.


## Serie
Eén niveau lager, dat van de verzameling van kranten met dezelfde titel, is een `ldto:Informatieobject` op het `ldto:aggregatieniveau` "*serie*". Deze "serie" is niet één-op-één gelijk aan een krantentitel. De "serie" is de *concrete deelverzameling van archiefstukken*, een (kranten-) titel is een abstractere bibliografische entiteit. Gesteld mag worden dat het `ldto:Informatieobject` betrekking heeft op de bibliografische krantentitel (als *groeperings-criterium*). Dit onderscheid leggen we als volgt vast:

    <https://data.razu.nl/id/object/NL-WbDRAZU-K50907905-1234-1>
        a ldto:Informatieobject ;
        ldto:aggregatieniveau <https://data.razu.nl/id/aggregatieniveau/cd4b9482eadd1fea35dbf01c9a05b093> ; # serie
        ldto:classificatie <https://data.razu.nl/id/soort/e7f8935f15730273e0b9ab9a0f74b2f8> ;               # krant
        ldto:naam "De Amerongse Courant" ;
        ldto:archiefvormer <https://data.razu.nl/id/actor/aafc151236a6978fdf1732dcadb53f2e> ;  # = Utrechtse Heuvelrug
        ldto:isOnderdeelVan <https://data.razu.nl/id/object/NL-WbDRAZU-K50907905-1234-0> ;
        # dekkingInTijd heeft betrekking op de verzameling van wat we beheren, niet wanneer de titel is uitgegeven: 
        ldto:dekkingInTijd [ 
            a ldto:DekkingInTijdGegevens ;     
            ldto:dekkingInTijdBeginDatum "1878"^^xsd:gYear ; 
            ldto:dekkingInTijdEindDatum "1929"^^xsd:gYear ;
            ldto:dekkingInTijdType <https://data.razu.nl/id/dekkingintijdtype/a3e30182626730af3b3c2a7071c58038> # = Verschijningsperiode 
        ] , [
            a ldto:DekkingInTijdGegevens ;
            ldto:dekkingInTijdBeginDatum "1941"^^xsd:gYear ; 
            ldto:dekkingInTijdEindDatum "1941"^^xsd:gYear ;  
            ldto:dekkingInTijdType <https://data.razu.nl/id/dekkingintijdtype/a3e30182626730af3b3c2a7071c58038> # = Verschijningsperiode 
        ] ;
        ldto:beperkingGebruik <https://data.razu.nl/id/licentie/c9ff6ea52d650cc82c5c04dd054aeb1f> ; # optioneel, in ieder geval op niveau aflevering
        ldto:dekkingInRuimte 
            <https://data.razu.nl/id/locatie/bf16fd9ceb0435731ea10b6e92c0848b>, # "Amerongen", 
            <https://data.razu.nl/id/locatie/152aa32fa903d3502880686e0d362668>, # "Leersum"
            <https://data.razu.nl/id/locatie/218bbb2e70cfce022ae09d6a4327b899>, # "Maarn"
            <https://data.razu.nl/id/locatie/a56c9792ea7d0614d0770b9bd46e3e56>, # "Maarsbergen" 
            <https://data.razu.nl/id/locatie/a4ed213e4fcc0888b2a88ab1a81847c4>, # "Doorn"
            <https://data.razu.nl/id/locatie/2f3d1d59d29f6f07ac921eb57fe37fbc>, # "Driebergen"
            <https://data.razu.nl/id/locatie/f43ef3ffcb8654ff73a672a05b88b404>, # "Langbroek"
            <https://data.razu.nl/id/locatie/f5ef414df02e8a28bb60055ff6e1c151>, # "Cothen"
            <https://data.razu.nl/id/locatie/d5acdcc4f873045aaefd2a31af723153>; # "Wijk bij Duurstede" 
        schema:mainEntity [
            # dit *is* de krantentitel in bibliografische zin:
            a schema:Newspaper ; 
            schema:name "De Amerongse Courant" ;
            schema:alternateName "Nieuws- en advertentieblad voor Amerongen, Leersum, Maarn, Maarsbergen, Doorn, Driebergen, Langbroek, Cothen, Wijk-bij-Duurstede enz" ;
            schema:spatialCoverage <https://data.razu.nl/id/locatie/bf16fd9ceb0435731ea10b6e92c0848b>, # "Amerongen", 
                <https://data.razu.nl/id/locatie/152aa32fa903d3502880686e0d362668>, # "Leersum"
                <https://data.razu.nl/id/locatie/218bbb2e70cfce022ae09d6a4327b899>, # "Maarn"
                <https://data.razu.nl/id/locatie/a56c9792ea7d0614d0770b9bd46e3e56>, # "Maarsbergen" 
                <https://data.razu.nl/id/locatie/a4ed213e4fcc0888b2a88ab1a81847c4>, # "Doorn"
                <https://data.razu.nl/id/locatie/2f3d1d59d29f6f07ac921eb57fe37fbc>, # "Driebergen"
                <https://data.razu.nl/id/locatie/f43ef3ffcb8654ff73a672a05b88b404>, # "Langbroek"
                <https://data.razu.nl/id/locatie/f5ef414df02e8a28bb60055ff6e1c151>, # "Cothen"
                <https://data.razu.nl/id/locatie/d5acdcc4f873045aaefd2a31af723153>; # "Wijk bij Duurstede" 
            schema:temporalCoverage "1870/1929", "1941" ;   # ISO 8601 incl. range '/'-aanduiding; geeft aan wanneer uitgekomen, dus niet per se gelijk aan de ldto:dekkingInTijd
            schema:publisher <https://data.razu.nl/id/actor/fdf07d26952c341ed9a70909eb3a4a73> ;  #  "B. Ruitenbeek - Doorn" ; 
            schema:inLanguage "nl" ;                        # conform IETF BCP 47
            schema:sameAs <EXTERNE_URIs_zoals_KB_catalogus_e.d> 
        ] ;
        dct:hasFormat <https://k50907905.opslag.razu.nl/NL-WbDRAZU-K50907905-1234-1.meta.json> . # locatie van deze metadata op de storage  


Het koppeling tussen de serie van archiefstukken die tot de zelfde titel behoren als de titel zelf, gebeurt hier via de `schema:mainEntity-relatie`. Bemerk dat de *dekkingInTijd* / *temporalCoverage*  kunnen verschillen omdat ze betrekking hebben op verschillende soorten entiteiten. Voor de volledigheid van de bibliografische beschrijving is er zowel een `ldto:dekkingInRuimte` als een `schema:spatialCoverage`, hoewel hun waarden overeenkomen.


## Archiefstuk
Één niveau lager is het `ldto:Informatieobject` een gearchiveerd *exemplaar* van een aflevering van het tijdschrift. Ook hier wordt de relatie tussen het concrete archiefstuk de abstractere bibliografische 'aflevering' gerepresenteerd via de `schema:mainEntity-relatie`:

    <https://data.razu.nl/id/object/NL-WbDRAZU-K50907905-1234-2>
        a ldto:Informatieobject ;
        ldto:aggregatieniveau <https://data.razu.nl/id/aggregatieniveau/96f7399fb1c5d3b7d2acdc48dac3d71e>;  # archiefstuk    
        ldto:classificatie <https://data.razu.nl/id/soort/30d2cbfabc5d7cf795d3ddb00b1e8260> ;               # aflevering (van seriële publicatie)
        ldto:naam "De Amerongse Courant, vol. 8, no. 52 (1929-12-28)" ;                                     # is dit een prettig formaat?
        ldto:archiefvormer <https://data.razu.nl/id/actor/aafc151236a6978fdf1732dcadb53f2e> ;               # Utrechtse Heuvelrug
        ldto:isOnderdeelVan <https://data.razu.nl/id/object/NL-WbDRAZU-K50907905-1234-1> ;
        ldto:raadpleeglocatie "hier aangeven waar dit issue in het depot te vinden is" ;                    # TODO formattering?
        ldto:dekkingInRuimte 
            <https://data.razu.nl/id/locatie/bf16fd9ceb0435731ea10b6e92c0848b>, # "Amerongen", 
            <https://data.razu.nl/id/locatie/152aa32fa903d3502880686e0d362668>, # "Leersum"
            <https://data.razu.nl/id/locatie/218bbb2e70cfce022ae09d6a4327b899>, # "Maarn"
            <https://data.razu.nl/id/locatie/a56c9792ea7d0614d0770b9bd46e3e56>, # "Maarsbergen" 
            <https://data.razu.nl/id/locatie/a4ed213e4fcc0888b2a88ab1a81847c4>, # "Doorn"
            <https://data.razu.nl/id/locatie/2f3d1d59d29f6f07ac921eb57fe37fbc>, # "Driebergen"
            <https://data.razu.nl/id/locatie/f43ef3ffcb8654ff73a672a05b88b404>, # "Langbroek"
            <https://data.razu.nl/id/locatie/f5ef414df02e8a28bb60055ff6e1c151>, # "Cothen"
            <https://data.razu.nl/id/locatie/d5acdcc4f873045aaefd2a31af723153>; # "Wijk bij Duurstede" 
        ldto:beperkingGebruik <https://data.razu.nl/id/licentie/c9ff6ea52d650cc82c5c04dd054aeb1f> ;
        schema:mainEntity [  
            a schema:PublicationIssue ;
            schema:name "De Amerongse Courant, vol. 8, no. 52 (1929-12-28)" ;                               # formaat beschrijving?? 
            schema:alternateName "Nieuws- en advertentieblad voor Amerongen, Leersum, Maarn, Maarsbergen, Doorn, Driebergen, Langbroek, Cothen, Wijk-bij-Duurstede enz" ;
            schema:datePublished "1929-12-28"^^xsd:date ;
            schema:isPartOf [
                a schema:PublicationVolume  ;
                schema:volumeNumber "8"         # = dit is het 8e  jaar dat deze titel uitgegeven wordt
            ] ;
            schema:numberOfPages 4;
            schema:issueNumber "52"             # - dit is de 52e aflevering van dit jaar
        ] ;
        dct:hasFormat <https://k50907905.opslag.razu.nl/NL-WbDRAZU-K50907905-1234-2.meta.json> . # locatie van deze metadata op de storage  

Voor de volledigheid van de beschrijving van het `ldto:Informatieobject` wordt ook hier de `ldto:dekkingInRuimte` opgenomen.


## Bestanden
Van een aflevering worden digitaal, als bestand, de pagina's bewaard. Om de metadata niet onnodig complex te maken, en verwarring te voorkomen dat een archiefstuk (aflevering) ook weer archiefstukken (digitale pagina's) bevat, modeleren we een pagina *niet* als een `ldto:Informatieobject` maar enkel als een `ldto:Bestand`. Het bestand biedt een representatie van de aflevering. Op pagina-niveau zijn meerdere representaties mogelijk, bijvoorbeeld de afbeelding (scan) of de alto-xml.

    <https://data.razu.nl/id/object/NL-WbDRAZU-K50907905-1234-4>
        a ldto:Bestand ;
        ldto:naam "NL-WbDRAZU-K50907905-1234-4.jpg" ;    # als hoger niveau + positie , of bestandsnaam?
        ldto:URLBestand <https://k50907905.opslag.razu.nl/NL-WbDRAZU-K50907905-1234-4.jpg> ;
        ldto:bestandsformaat <https://data.razu.nl/id/bestandsformaat/84621bf26697a4a776a9007b97023412> ;  # jp2
        ldto:checksum [ a ldto:ChecksumGegevens ;
            ldto:checksumAlgoritme <https://data.razu.nl/id/algoritme/7f138a09169b250e9dcb378140907378> ;
            ldto:checksumDatum "2025-01-13T10:28:59.004406+00:00"^^xsd:dateTime ;
            ldto:checksumWaarde "c2c90c72aa8516a171324793cba37407" ] ;
        ldto:isRepresentatieVan <https://data.razu.nl/id/object/NL-WbDRAZU-K50907905-1234-2> ;
        ldto:omvang 370539 ;
        iiif:service <https://iiif.example.com/iiif/issue1/page1> ;     # nader te bepalen IIIF Image API Endpoint
        schema:width 4000 ;
        schema:height 6000 ;
        schema:position 1 ;
        dct:hasFormat <https://k50907905.opslag.razu.nl/NL-WbDRAZU-K50907905-1234-4.meta.json> . 


Bovenstaande geeft de afbeelding van pagina 1. Het is herkenbaar als afbeelding door het `ldto:bestandsformaat` en dat een breedte en een hoogte gegeven zijn (in pixels, via `schema:width` en `schema:height`). In aanvulling op de URI van het object, de locatie op de S3 (`ldto:URLBestand`) en locatie van deze metadata op de S3 (`dct:hasFormat`) biedt deze metadata ook de IIIF-URI (`iiif:service`) van de afbeelding zoals beschikbaar via de (nog in te richten IIIF-service).

Als het bestand representatief zou zijn voor het volledige exemplaar van de aflevering, dan zou attribuut `schema:position` ontbreken.
Als het bestand een alto-xml zou zijn, dan zou dat indirect herleid kunnen worden aan het `ldto:bestandsformaat` ("xml") en aan de extensie in `ldto:URLBestand` (eingdigt op "alto.xml"). Daarnaast zou het object geen attributen `schema:width`, `schema:height` of `iiif.service` bevatten. Hier volgt een voorbeeld van een PDF van de complete aflevering een een voorbeeld van een alt-xml:

    <https://data.razu.nl/id/object/NL-WbDRAZU-K50907905-1234-3>
        a ldto:Bestand ;
        ldto:naam "NL-WbDRAZU-K50907905-1234-3.pdf" ;    # een bestand heeft als naam de bestandsnaam :-)
        ldto:URLBestand <https://k50907905.opslag.razu.nl/NL-WbDRAZU-K50907905-1234-3.pdf> ;
        ldto:bestandsformaat <https://data.razu.nl/id/bestandsformaat/84621bf26697a4a776a9007b97023412> ;  # pdf
        ldto:checksum [ a ldto:ChecksumGegevens ;
            ldto:checksumAlgoritme <https://data.razu.nl/id/algoritme/7f138a09169b250e9dcb378140907378> ;
            ldto:checksumDatum "2025-01-13T10:28:59.004406+00:00"^^xsd:dateTime ;
            ldto:checksumWaarde "c2c90c72aa8516a171324793cba37407" ] ;
        ldto:isRepresentatieVan <https://data.razu.nl/id/object/NL-WbDRAZU-K50907905-1234-2> ;
        ldto:omvang 370539 ;
        dct:hasFormat <https://k50907905.opslag.razu.nl/NL-WbDRAZU-K50907905-1234-3.meta.json> . # locatie van deze metadata op de storage  

    <https://data.razu.nl/id/object/NL-WbDRAZU-K50907905-1234-5>
        a ldto:Bestand ;
        ldto:naam "NL-WbDRAZU-K50907905-1234-5.alto.xml" ;
        ldto:URLBestand <https://k50907905.opslag.razu.nl/NL-WbDRAZU-K50907905-1234-5.alto.xml> ;
        ldto:bestandsformaat <https://data.razu.nl/id/bestandsformaat/84621bf26697a4a776a9007b97023412> ;  # xml;
        ldto:checksum [ a ldto:ChecksumGegevens ;
            ldto:checksumAlgoritme <https://data.razu.nl/id/algoritme/7f138a09169b250e9dcb378140907378> ;
            ldto:checksumDatum "2025-01-13T10:28:59.004406+00:00"^^xsd:dateTime ;
            ldto:checksumWaarde "c2c90c72aa8516a171324793cba37407" ] ;
        ldto:isRepresentatieVan <https://data.razu.nl/id/object/NL-WbDRAZU-K50907905-1234-2> ;
        ldto:omvang 370539 ;
        schema:position 1 ;
        dct:hasFormat <https://k50907905.opslag.razu.nl/NL-WbDRAZU-K50907905-1234-5.meta.json> . 


