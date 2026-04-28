---
title: "Chapter 5 Viruses, HIV and Drug Resistance | From sequences to knowledge, improving and learning from sequence alignments"
source: "https://thesis.lucblassel.com/viruses-hiv-and-drug-resistance.html"
author:
  - "[[Luc Blassel]]"
published:
created: 2026-04-26
description: "Chapter 5 Viruses, HIV and Drug Resistance | From sequences to knowledge, improving and learning from sequence alignments"
tags: []
---
## Chapter 5 Viruses, HIV and Drug Resistance

## 5.1 What are viruses?

Viruses occupy a strange place in the tree of life, with many debating if they are actually alive or not. André Lwoff gave what is probably the most fitting definition: *“viruses are viruses”* <sup><a href="#ref-lwoffConceptVirus1957" role="doc-biblioref">424</a></sup>. Despite this ambiguity, viruses share some common characteristics which allow us to define them as intracellular parasites <sup><a href="#ref-minorViruses2014" role="doc-biblioref">425</a></sup>:

1. Viruses have some type of genetic information, contained in DNA or RNA.
2. This genetic information is protected by some form of envelope.
3. They use the cellular machinery of host cells to make copies of themselves.

While we all know that viruses can be pathogenic and dangerous (the recent example of SARS-CoV2 springs to mind), that is not necessarily the case. Some viruses like GBV-C <sup><a href="#ref-stapletonGBVirusesReview2011" role="doc-biblioref">426</a></sup> or certain strains of H5N1 *Influenza* <sup><a href="#ref-yamamotoCharacterizationNonpathogenicH5N12011" role="doc-biblioref">427</a></sup> are non pathogenic and essentially harmless.

Viruses have been discovered for all three domains of life: Eukaryota, Bacteria and Archea. In Eukaryota many viruses have been discovered for animals (both vertebrate <sup><a href="#ref-shiEvolutionaryHistoryVertebrate2018" role="doc-biblioref">428</a></sup> and invertebrate <sup><a href="#ref-adamsAtlasInvertebrateViruses2017" role="doc-biblioref">429</a></sup>), plants <sup><a href="#ref-lefeuvreEvolutionEcologyPlant2019" role="doc-biblioref">430</a></sup>, protozoa <sup><a href="#ref-wangVirusesParasiticProtozoa1991" role="doc-biblioref">431</a></sup>, chromista <sup><a href="#ref-ferminVirusesProkaryotesProtozoa2018" role="doc-biblioref">432</a></sup> and even fungi <sup><a href="#ref-sutelaVirusesFungiOomycetes2019" role="doc-biblioref">433</a></sup>. Bacterial viruses known as phages have been known to exists since the beginning of the 20th century <sup><a href="#ref-twortINVESTIGATIONNATUREULTRAMICROSCOPIC1915" role="doc-biblioref">434</a>,<a href="#ref-delbrockBacterialVirusesBacteriophages1946" role="doc-biblioref">435</a></sup>. These bacteriophages are being considered as a therapeutic alternative to antibiotics <sup><a href="#ref-clarkBacterialVirusesHuman2004" role="doc-biblioref">436</a>,<a href="#ref-vankan-davelaarUsingVirusesNanomedicines2014" role="doc-biblioref">437</a></sup> which could help with multi-drug-resistant bacterial pathogens. Archea are also known to have their own viral infections <sup><a href="#ref-prangishviliVirusesArchaea2016" role="doc-biblioref">438</a>,<a href="#ref-prangishviliVirusesArchaeaUnifying2006" role="doc-biblioref">439</a></sup>.

Strangely even viruses of viruses seem to exist, such as the plant satellite virus <sup><a href="#ref-franckiPlantVirusSatellites" role="doc-biblioref">440</a>,<a href="#ref-xuPlantVirusSatellites2011" role="doc-biblioref">441</a></sup> or hepatitis delta virus <sup><a href="#ref-laiMolecularBiologyHepatitis1995" role="doc-biblioref">442</a>,<a href="#ref-hughesHepatitisDeltaVirus2011" role="doc-biblioref">443</a></sup>. These “viroids” do not infect viral hosts *per se* but they cannot replicate on their own. Replication must happen during co-infection with a larger virus. More recently, true viruses of viruses called virophages have been discovered. These virophages like sputnik <sup><a href="#ref-desnuesChapterSputnikVirophage2012" role="doc-biblioref">444</a></sup> or zamilon <sup><a href="#ref-gaiaZamilonNovelVirophage2014" role="doc-biblioref">445</a></sup> specifically infect giant viruses.

There is a huge diversity of viruses affecting all types of life, and new viruses are being discovered all the time <sup><a href="#ref-edgarPetabasescaleSequenceAlignment2022" role="doc-biblioref">446</a></sup>. This diversity hints at a rich and long evolutionary history. When and where viruses originated is still under study <sup><a href="#ref-nasirInvestigatingConceptOrigin2020" role="doc-biblioref">447</a>,<a href="#ref-forterreOriginViruses2009" role="doc-biblioref">448</a></sup> and we might never know how they emerged. It is, however, believed that they may have played an important role in the emergence of eukaryotic cells <sup><a href="#ref-forterreOriginVirusesTheir2006" role="doc-biblioref">449</a></sup>. This co-evolution between virus and host cell shows a strong link between the two organisms and some parts of the human genome are likely of ancient viral origin <sup><a href="#ref-boekeRetrotransposonsEndogenousRetroviruses1997" role="doc-biblioref">450</a>,<a href="#ref-kojimaViruslikeInsertionsSequence2021" role="doc-biblioref">451</a></sup>. It has been estimated that 1% to 8% of the human genome are endogenous retroviral sequences <sup><a href="#ref-lowerVirusesAllUs1996" role="doc-biblioref">452</a>,<a href="#ref-griffithsEndogenousRetrovirusesHuman2001" role="doc-biblioref">453</a></sup>.

The rich diversity of viruses is reflected in the variety of genetic information support, replication strategy, physical and genomic size, as well as shape. The differences in genetic information support and replication strategy form the basis of the Baltimore virus classification system <sup><a href="#ref-baltimoreExpressionAnimalVirus1971" role="doc-biblioref">454</a></sup>, still used today <sup><a href="#ref-kooninBaltimoreClassificationViruses2021" role="doc-biblioref">455</a></sup> to classify virus lineages.

As stated above, all viruses have some genetic information. This information is stored either as DNA or as RNA, which is the molecule of choice for 70% of human pathogenic viruses <sup><a href="#ref-domingoRNAVirusGenomes2018" role="doc-biblioref">456</a></sup> (HIV and SARS-CoV 2 are RNA viruses).

For DNA viruses, the molecule can be double-stranded as for *Herpesvirus* <sup><a href="#ref-mcgeochTopicsHerpesvirusGenomics2006" role="doc-biblioref">457</a>,<a href="#ref-boehmerHerpesVirusReplication2003" role="doc-biblioref">458</a></sup>, single-stranded like in the case of *Papillomavirus* <sup><a href="#ref-brentjensHumanPapillomavirusReview2002" role="doc-biblioref">459</a></sup> or even circular in the case of the Hepatitis B virus <sup><a href="#ref-kayHepatitisVirusGenetic2007" role="doc-biblioref">460</a></sup>. This molecular diversity is also present in RNA viruses where the RNA molecule can be double-stranded like for *Rotavirus* <sup><a href="#ref-parasharRotavirus1998" role="doc-biblioref">461</a></sup>, or single-stranded. Furthermore, for single-stranded RNA viruses the strand can either be positive (*i.e.* can be directly translated into a protein) like the Hepatitis C virus <sup><a href="#ref-simmondsVariabilityHepatitisVirus1995" role="doc-biblioref">462</a></sup> or *Poliovirus* <sup><a href="#ref-wimmerGeneticsPoliovirus1993" role="doc-biblioref">463</a>,<a href="#ref-racanielloOneHundredYears2006" role="doc-biblioref">464</a></sup>; conversely there are negative-strand RNA viruses, for which the complementary strand of RNA must be synthesized before translation into a protein, such as the Influenza or Measles viruses <sup><a href="#ref-paleseNegativestrandRNAViruses1996" role="doc-biblioref">465</a></sup>.

This diversity in genetic information support implies a necessary diversity in replication strategy. The main replication strategies are as follows <sup><a href="#ref-domingoVirusEvolution2014" role="doc-biblioref">466</a></sup>:

Finally, the genetic diversity of viruses is reflected in their physical characteristics: viruses come in all shapes and sizes. Physical size range from 17nm for plant satellite viruses <sup><a href="#ref-pyleChapter58Biology2017" role="doc-biblioref">473</a></sup> to the giant, 400nm *Mimivirus* <sup><a href="#ref-raoult2megabaseGenomeSequence2004" role="doc-biblioref">474</a></sup>. Genomic size is also quite variable. There is a stark contrast between the 860 bp *Circovirus SFBeef* and the 2.5 Mbp *Pandoravirus salinus* genomes <sup><a href="#ref-campillo-balderasViralGenomeSize2015" role="doc-biblioref">475</a></sup>. Viruses also come in a variety of shapes <sup><a href="#ref-cannVirusStructure2015" role="doc-biblioref">476</a></sup>: icosahedral for HIV, helical for the tobacco mosaic virus or a distinctive head-tail shape for bacteriophages.

Although there are a large number of viruses, and many of them are of great importance for human health, we will now focus on one virus of particular importance: Human Immunodeficiency Virus otherwise known as HIV.

## 5.2 Getting to know HIV

### 5.2.1 Quick presentation of HIV

HIV is a single-stranded RNA retrovirus that is responsible for the Acquired Immune Deficiency Syndrome (AIDS) pandemic that has been around for the last couple decades. This virus is transmitted through sexual contact or through blood. Sexual activity is the largest transmission factor followed by intravenous drug use <sup><a href="#ref-hladikSettingStageHost2008" role="doc-biblioref">477</a>,<a href="#ref-shawHIVTransmission2012" role="doc-biblioref">478</a></sup>.

HIV infects cells of the host immune system, specifically CD4 T-cell lymphocytes and destroys them due to its replication process <sup><a href="#ref-weissHowDoesHIV1993" role="doc-biblioref">479</a></sup>. CD4 T-cells are an essential part of the immune system response, helping fight against infection in humans. An HIV infection typically starts with an asymptomatic phase that can last years, followed by a growth in viral replication leading to a decrease in CD4 cells which progresses into AIDS <sup><a href="#ref-melhuishNaturalHistoryHIV2018" role="doc-biblioref">480</a></sup>. During AIDS, when the CD4 cell count is low enough, opportunistic diseases such as pneumonia or tuberculosis <sup><a href="#ref-murrayPulmonaryComplicationsAcquired1984" role="doc-biblioref">481</a></sup> can easily infect the host, leading to death when the immune system is weak enough.

HIV/AIDS is one of the deadliest pandemics in history, estimated to have lead to the death of 36 million people <sup><a href="#ref-sampathPandemicsThroughoutHistory2021" role="doc-biblioref">482</a></sup>. In 2010 approximately 33 million people were infected with HIV <sup><a href="#ref-worldhealthorganizationGlobalReportUNAIDS2010" role="doc-biblioref">483</a></sup>, 2.6 million of which were due to new infections, and 1.8 million died of AIDS. Most of the new infections happened in economically developing regions of the world, 70% of them coming from sub-Saharan Africa <sup><a href="#ref-worldhealthorganizationGlobalReportUNAIDS2010" role="doc-biblioref">483</a></sup>. As of 2020, these numbers have decreased with “only” 1.5 million new infections and 680,000 AIDS deaths, which is encouraging from a public health perspective.

The HIV-1 virus was discovered simultaneously in 1983 by Françoise Barré-Sinoussi, Luc Montagnier <sup><a href="#ref-barre-sinoussiIsolationTlymphotropicRetrovirus1983" role="doc-biblioref">484</a></sup> and Robert Gallo <sup><a href="#ref-galloIsolationHumanTcell1983" role="doc-biblioref">485</a></sup>. There exists a second HIV-2 virus discovered shortly after HIV-1 <sup><a href="#ref-clavelIsolationNewHuman1986" role="doc-biblioref">486</a></sup>, it is however less transmissible than HIV-1 which is largely responsible for the global HIV/AIDS pandemic <sup><a href="#ref-gilbertComparisonHIV1HIV22003" role="doc-biblioref">487</a></sup>. In Africa in 2006, HIV-1 infections were rising where HIV-2 were declining <sup><a href="#ref-vanderloeffSixteenYearsHIV2006" role="doc-biblioref">488</a></sup>.

While both viruses are of zoonotic origin, from transmissions of Simian Immunodeficiency Virus (SIV) from primates to humans, HIV-1 most likely originates from an SIV present in chimpanzees <sup><a href="#ref-gaoOriginHIV1Chimpanzee1999" role="doc-biblioref">489</a> – <a href="#ref-sharpOriginsHIVAIDS2011" role="doc-biblioref">491</a></sup>, and HIV-2 from an SIV present in Sooty mangabeys <sup><a href="#ref-hirschAfricanPrimateLentivirus1989" role="doc-biblioref">492</a> – <a href="#ref-chenGeneticCharacterizationNew1996" role="doc-biblioref">494</a></sup>.

Several independent such transmissions have resulted in 4 lineages of HIV-1 labeled groups M, N, O and P <sup><a href="#ref-hemelaarOriginDiversityHIV12012" role="doc-biblioref">495</a></sup> (similarly HIV-2 is split into groups A to H also resulting from independent zoonotic transmissions). Groups N and P have been identified in only a handful of individuals in Cameroon, and group O is estimated to a few thousand cases in western Africa. The majority of the pandemic is due to viruses from group M.

The most recent common ancestor, *i.e.* the putative virus that founded group M, is estimated to have originated in what is now the Democratic Republic of Congo <sup><a href="#ref-worobeyDirectEvidenceExtensive2008" role="doc-biblioref">496</a> – <a href="#ref-fariaEarlySpreadEpidemic2014" role="doc-biblioref">498</a></sup> at some point between 1910 and 1931 <sup><a href="#ref-worobeyDirectEvidenceExtensive2008" role="doc-biblioref">496</a>,<a href="#ref-korberTimingAncestorHIV12000" role="doc-biblioref">499</a>,<a href="#ref-rambautCausesConsequencesHIV2004" role="doc-biblioref">500</a></sup>.

Group M is further subdivided into 9 subtypes each with distinct genetic characteristics, labeled A to K <sup><a href="#ref-sharpOriginsHIVAIDS2011" role="doc-biblioref">491</a>,<a href="#ref-mccutchanGlobalEpidemiologyHIV2006" role="doc-biblioref">501</a></sup>. Like in many viruses <sup><a href="#ref-perez-losadaRecombinationVirusesMechanisms2015" role="doc-biblioref">502</a></sup>, when 2 genetically different strains of HIV co-infect a single host there is a risk of genetic recombination leading to a new strain <sup><a href="#ref-robertsonRecombinationAIDSViruses1995" role="doc-biblioref">503</a></sup>. During recombination, a new genome is formed from parts of the original genomes. This can lead to new strains that can spread and form lineages of their own. HIV strains resulting from recombination are called Circulating Recombinant Forms (CRFs). There are currently 118 identified HIV-1 CRFs in the Los Alamos National Laboratory HIV sequence database <sup><a href="#ref-HIVCirculatingRecombinant" role="doc-biblioref">504</a></sup> (1 for HIV-2). Many unique recombinant forms (URFs) also exist. URFs and CRFs are both the result of intra-host genetic recombination a URF becomes a CRF once it has been identified in at least three epidemiologically independent infected individuals <sup><a href="#ref-lauCurrentTrendsHIV2013" role="doc-biblioref">505</a></sup>. Recombination can be particularly bothersome, complicating evolutionary analyses <sup><a href="#ref-posadaRecombinationEvolutionaryGenomics2002" role="doc-biblioref">506</a></sup>, facilitating the emergence of drug resistance and hindering vaccine development <sup><a href="#ref-taylorChallengeHIV1Subtype2008" role="doc-biblioref">507</a></sup>.

While subtype C represented almost half of global infections from 2004 to 2007, subtype B is the majority subtype in richer countries of North America and Western Europe <sup><a href="#ref-hemelaarGlobalTrendsMolecular2011" role="doc-biblioref">508</a></sup> where sequencing efforts are more common. This accounts for an over-representation of subtype B sequences in public databases such as the Los Alamos sequence database where 54% of sequences are of the B subtype and only 15% are C <sup><a href="#ref-DistributionAllHIV1" role="doc-biblioref">509</a></sup>.

### 5.2.2 The replication cycle of HIV

The virus’s replication cycle and its immune-cell host specificity are what makes it particularly dangerous. This replication cycle can broadly be categorized into 9 separate steps <sup><a href="#ref-freedHIV1Replication2001" role="doc-biblioref">510</a>,<a href="#ref-fergusonHIV1ReplicationCycle2002" role="doc-biblioref">511</a></sup> shown in Figure [5.1](https://thesis.lucblassel.com/viruses-hiv-and-drug-resistance.html#fig:hivCycle).

1. An HIV virion binds itself to the CD4 host cell through membrane proteins.
2. The virion envelope and host cell membrane fuse together, allowing the viral genetic material and proteins to enter the host cell.
3. The viral RNA is reverse-transcribed into viral DNA.
4. The viral DNA is integrated into the host cell genome.
5. The integrated viral DNA is transcribed by the host cell machinery into multiple copies of viral RNA.
6. The viral RNA is translated into immature viral polyproteins.
7. The viral polyproteins are cleaved to form individual viral proteins.
8. The newly synthesized viral RNA and viral proteins gather around the host-cell membrane which starts budding to create a new virion.
9. Once the budding is complete, the virion is released from the host cell and matures before being able to infect other CD4 cells and replicate again.

The successive infection of CD4 cells by HIV virions leads to cellular death due to inflammatory response and/or activation of apoptosis <sup><a href="#ref-gougeonDirectIndirectMechanisms1993" role="doc-biblioref">512</a>,<a href="#ref-vidyavijayanPathophysiologyCD4TCell2017" role="doc-biblioref">513</a></sup>. The gradual depletion of CD4 cells in the infected individual’s body lead to the suppression of the immune system, and eventually to AIDS.

![**Main steps of HIV-1 replication cycle.**  
The HIV virion contains viral RNA and three essential proteins: Reverse Transcriptase (RT) represented in red, Integrase (IN) represented in cyan and Protease (PR) represented in yellow.
](https://thesis.lucblassel.com/figures/HIV-Intro/HIV-cycle.png)

Figure 5.1: **Main steps of HIV-1 replication cycle.**  
The HIV virion contains viral RNA and three essential proteins: Reverse Transcriptase (RT) represented in red, Integrase (IN) represented in cyan and Protease (PR) represented in yellow.

### 5.2.3 Genetics of HIV

The replication cycle described in Section [5.2.2](https://thesis.lucblassel.com/viruses-hiv-and-drug-resistance.html#the-replication-cycle-of-hiv) is made possible by the 15 proteins of HIV. These proteins are coded by 9 separate genes <sup><a href="#ref-frankelHIV1FifteenProteins1998" role="doc-biblioref">514</a></sup>. An overview of the HIV proteins, their structure and localization within the viral particle can be seen in Figure [5.2](https://thesis.lucblassel.com/viruses-hiv-and-drug-resistance.html#fig:hivStructure).

The HIV genome is made up of three main genes each coding for polyproteins and six genes coding for proteins with regulatory or accessory roles. The three polyproteins correspond to long chains of amino acids which are subsequently cleaved at specific positions to produce separate viral proteins.

The *gag* (“group-specific-antigen”) gene codes for the Gag polyprotein which, once cleaved, results in four proteins with mainly structural roles:

- The Matrix protein (MA or p17) lines the internal surface of the virion membrane, maintaining the shape and structural integrity of the virion.
- The Capsid protein (CA or p24) forms an inner core (the capsid) inside the virion around the viral RNA. It helps protect the viral genetic information.
- The Nucleocapsid protein (NC or p7) binds with the viral RNA inside the capsid, stabilizing the molecule and further protecting the genetic information.
- The p6 protein is a small, largely unstructured protein <sup><a href="#ref-fossenSolutionStructureHuman2005" role="doc-biblioref">515</a></sup> that is suspected of playing a role in virion budding and release from the host cell at the end of the replication cycle <sup><a href="#ref-gottlingerEffectMutationsAffecting1991" role="doc-biblioref">516</a>,<a href="#ref-huangP6GagRequiredParticle1995" role="doc-biblioref">517</a></sup>.

The *pol* (“polymerase”) gene codes for the Pol polyprotein. After cleaving, this results in three essential viral enzymes at the heart of the replication cycle:

- The Protease (PR) is responsible for cleaving the Gag, Pol and Env polyproteins to get the individual viral proteins. Without it, the individual viral proteins cannot come into being and therefore cannot function, stopping viral replication.
- The Reverse Transcriptase (RT or p51/p66) is responsible for synthesizing viral DNA from the viral RNA template contained in the virion. This is the first step in hijacking the cellular machinery for replication. Without viral DNA, HIV replication is impossible.
- The Integrase (IN) is responsible for integrating the viral DNA produced by RT in to the host cell DNA. Once the viral DNA is inside the host genome it can be transcribed and then translated (as described in Section [1.1](https://thesis.lucblassel.com/what-is-sequence-data.html#biological-sequences-a-primer)) to produce new copies of the viral RNA and proteins. Without this integration step the viral genetic information cannot be expressed and the replication cycle is stopped.

These three proteins are of particular importance and we will go into more detail about them in Section [5.3.2](https://thesis.lucblassel.com/viruses-hiv-and-drug-resistance.html#drug-mechanisms).

The *env* (“envelope”) gene codes for Env, the third and last polyprotein. The two resulting proteins coat the membrane of the virion and are responsible for binding with the CD4 host cells.

- The Surface protein (SU or gp120) binds to receptors on the surface of CD4 cells and allows the virion to attach itself to the host cell <sup><a href="#ref-bourHumanImmunodeficiencyVirus1995" role="doc-biblioref">518</a></sup>. It also enables membrane fusion, the essential first step in the viral replication cycle <sup><a href="#ref-hernandezViruscellCellcellFusion1996" role="doc-biblioref">519</a></sup>.
- The Transmembrane protein (TM or gp41) anchors SU into the virion membrane.

The 6 remaining genes all code for single proteins. Two of these have essential regulatory roles and the remaining four accessory roles.

The *tat* (“trans-activator of transcription”) gene codes for Tat, the first essential regulatory protein. Tat activates and promotes transcription leading to more numerous and longer copies of the viral RNA <sup><a href="#ref-jonesControlRnaInitiation1994" role="doc-biblioref">520</a></sup>. The *rev* (for “regulator of virion”) gene codes for Rev, the second essential regulatory protein. Rev helps transcribed viral RNA exit the nucleus of the host cell in order to be translated to viral proteins or be packaged in new, budding virions <sup><a href="#ref-hopeViralRNAExport1997" role="doc-biblioref">521</a></sup>.

The remaining four accessory genes are as follows: *nef* (“negative regulatory factor”) code for the Nef protein which prevents the production of the CD4 cellular defense proteins increasing infectivity <sup><a href="#ref-mangasarianMultifacetedRoleHIV1997" role="doc-biblioref">522</a></sup>; *vif* (“viral infectivity factor”) codes for the Vif protein which also increases viral infectivity <sup><a href="#ref-cohenRoleAuxiliaryProteins1996" role="doc-biblioref">523</a></sup>; *vpu* (“viral protein U”) codes for Vpu which likely helps during release of new virions <sup><a href="#ref-cohenRoleAuxiliaryProteins1996" role="doc-biblioref">523</a>,<a href="#ref-lambVpuVprHuman1997" role="doc-biblioref">524</a></sup> as well as preventing production of CD4 in the host cell. It is not believed to be present in the mature virion as it binds to host cellular membranes <sup><a href="#ref-khanRoleViralProtein2021" role="doc-biblioref">525</a></sup>; *vpr* (“viral protein R”) likely helps viral DNA enter the host cell nucleus and prevents the natural host cell reproduction cycle <sup><a href="#ref-emermanHIV1VprCell1996" role="doc-biblioref">526</a></sup>.

The existence of a 10th HIV-1 gene was suggested in 1988 <sup><a href="#ref-millerHumanImmunodeficiencyVirus1988" role="doc-biblioref">527</a></sup>, overlapping the *env* gene and coding for proteins on the other strand of viral DNA than the other genes. This putative gene was named *asp* (“antisense protein”) and Asp transcripts were isolated during an HIV-1 infection in 2002 <sup><a href="#ref-briquetImmunolocalizationStudiesAntisense2002" role="doc-biblioref">528</a></sup>. The function of this protein is still unknown but it has been shown to have a strong evolutionary correlation with HIV-1 group M responsible for the pandemic <sup><a href="#ref-cassanConcomitantEmergenceAntisense2016" role="doc-biblioref">529</a></sup>. This Asp protein is still a source of debate and is under active research <sup><a href="#ref-savoretPilotStudyHumoral2020" role="doc-biblioref">530</a></sup>.

![**Structure and main components of a mature HIV-1 virion.**  
Structural proteins MA, CA, SU and TM are represented in Blue, functional enzymes RT, IN and PR in pink, RNA binding proteins Rev, Tat and NC in orange and accessory proteins Vif, Nef, Vpr and Vpu in green. Viral RNA is shown in yellow. The phospholipd membrane of the virion is shown in a light purple color. The p6 protein is not represented as it is largely unsctructured. Vpu is not believed to be present in the HIV virion.  
Figure adapted from PDB101 [@zardeckiPDB101EducationalResources2022] ([PDB101.rcsb.org](https://PDB101.rcsb.org), *CC By 4.0 License*, detailed list of structures used available in Appendix \@ref(HIV-intro-appendix)).](https://thesis.lucblassel.com/figures/HIV-Intro/HIV-structure.png)

Figure 5.2: **Structure and main components of a mature HIV-1 virion.**  
Structural proteins MA, CA, SU and TM are represented in Blue, functional enzymes RT, IN and PR in pink, RNA binding proteins Rev, Tat and NC in orange and accessory proteins Vif, Nef, Vpr and Vpu in green. Viral RNA is shown in yellow. The phospholipd membrane of the virion is shown in a light purple color. The p6 protein is not represented as it is largely unsctructured. Vpu is not believed to be present in the HIV virion.  
Figure adapted from PDB101 <sup><a href="#ref-zardeckiPDB101EducationalResources2022" role="doc-biblioref">531</a></sup> ([PDB101.rcsb.org](https://pdb101.rcsb.org/), *CC By 4.0 License*, detailed list of structures used available in Appendix [B](https://thesis.lucblassel.com/HIV-intro-appendix.html#HIV-intro-appendix)).

## 5.3 Drug resistance in HIV

Although the HIV/AIDS pandemic has been very deadly around the world, we are not completely defenseless against it. The first antiretroviral therapy (ART) drugs were made available in the late eighties, only a couple years after discovering the virus. ART reduce the viral load in an HIV positive patient reducing its transmissibility <sup><a href="#ref-eisingerHIVViralLoad2019" role="doc-biblioref">532</a></sup>. While ART is not a cure for an HIV infection it has been shown to drastically reduce mortality and morbidity <sup><a href="#ref-palellaDecliningMorbidityMortality1998" role="doc-biblioref">533</a></sup>. ART is estimated to have saved the lives of 9.5 million individuals between 1995 and 2015 <sup><a href="#ref-forsytheTwentyYearsAntiretroviral2019" role="doc-biblioref">534</a></sup>.

### 5.3.1 A quick history of ART

The first available anti-HIV drug was Zidovudine (ZDV, also known as azidothymidine or AZT) approved by the FDA for usage in the USA in 1987 <sup><a href="#ref-fischlEfficacyAzidothymidineAZT1987" role="doc-biblioref">535</a></sup>, a few years only after the discovery of the virus. This drug was a reverse transcriptase inhibitor (RTI) therefore preventing the viral RNA from being transcribed into viral DNA. Unfortunately, 3 years later, strains of HIV resistant to ZDV were circulating <sup><a href="#ref-richmanSusceptibilityNucleosideAnalogues1990" role="doc-biblioref">536</a></sup>. This rapid emergence of resistance to treatment is common for HIV <sup><a href="#ref-yeoDeterminationHIV1RT2020" role="doc-biblioref">537</a></sup> due to its very high evolution rate <sup><a href="#ref-cuevasExtremelyHighMutation2015" role="doc-biblioref">538</a></sup> allowing it to explore many possible mutations in response to selective pressures, as well as the frequent occurrence of genetic recombination <sup><a href="#ref-carvajal-rodriguezRecombinationFavorsEvolution2007" role="doc-biblioref">539</a></sup>. To counter this resistance new drugs were rapidly developed and, between 1988 and 1995, four more RTIs were approved by the FDA. Using a combination of these drugs was also shown to be effective and led to a slower rise of resistance <sup><a href="#ref-gulickTreatmentIndinavirZidovudine1997" role="doc-biblioref">540</a></sup>.

Then, focus was shifted to the development of a new type of drug: Protease Inhibitors (PI). Between 1995 and 1997, 4 of them were approved. These, taken in combination with RTI made it harder for the virus to develop resistance <sup><a href="#ref-wensingFifteenYearsHIV2010" role="doc-biblioref">541</a></sup>. A new class of RTIs was also explored, Non-Nucleoside RTIs (NNRTIs) that block the RT action in another manner than the previously approved Nucleoside RTIs (NRTIs). When taken in combination with other drugs they are also highly effective <sup><a href="#ref-pedersenNonNucleosideReverseTranscriptase1999" role="doc-biblioref">542</a></sup>. As the years advanced even more drug targets were explored, with 5 Integrase inhibitors (INSTI) being approved since 2007 <sup><a href="#ref-scarsiHIV1IntegraseInhibitors2020" role="doc-biblioref">543</a></sup>, A Fusion Inhibitor (FI) in 2003 <sup><a href="#ref-fletcherEnfuvirtideNewDrug2003" role="doc-biblioref">544</a></sup>, and 3 other Entry inhibitors (EI) <sup><a href="#ref-esteHIVEntryInhibitors2007" role="doc-biblioref">545</a>,<a href="#ref-kilbyNovelTherapiesBased2003" role="doc-biblioref">546</a></sup> since 2007 all targeting different steps in the replication cycle of HIV (see Table [B.1](https://thesis.lucblassel.com/HIV-intro-appendix.html#tab:tableDrugs) and Figure [5.3](https://thesis.lucblassel.com/viruses-hiv-and-drug-resistance.html#fig:timeline)).

In response to the rapid emergence of resistance in HIV when treated with a single drug, clinicians started systematically treating HIV with a combination of multiple drugs targeting different proteins, as early as 1996. This is now referred to as highly active antiretroviral combination therapy (HAART, also known as tritherapy). HAART usually consists of 2 NRTIs coupled with another drug: NNRTI or PI at first and later FI or INSTI <sup><a href="#ref-yeniUpdateHAARTHIV2006" role="doc-biblioref">547</a></sup>. As of 2008, 22 anti-HIV single drugs were approved by the FDA <sup><a href="#ref-palmisanoBriefHistoryAntiretroviral2011" role="doc-biblioref">548</a></sup>, and 27 as of today. This large array of available drugs made HAART possible and gave options to clinicians to switch targets when the multi-resistant HIV emerged. It is important to note here that, while high-income countries had access to this large panel of antiviral drugs, in most lower-income countries that was not the case. This meant that drug switching and second-line [^1] drug regimens were rarely possible in these countries, leading to multi-resistant viruses <sup><a href="#ref-penningsHIVDrugResistance2013" role="doc-biblioref">549</a></sup>.

With the advent of HAART, patients had access to more potent treatments. However, the complexity of treatment regimens grew. They often involved several pills a day, taken at precise intervals. Complex drug regimens have been associated with poorer treatment adherence <sup><a href="#ref-mehtaPotentialFactorsAffecting1997" role="doc-biblioref">550</a>,<a href="#ref-millerComplianceTreatmentRegimens1997" role="doc-biblioref">551</a></sup>. This can lead to poor treatment outcome, as well as the emergence of multi-resistant HIV strains <sup><a href="#ref-chesneyAdherenceHIVCombination2000" role="doc-biblioref">552</a></sup> and their spread within the population. To avoid this issue, increasingly more single pill regimens are being developed with a staggering 7 new drugs approved by the FDA in 2018. These single pill regimens greatly reduce the burden of adherence for patients, leading to better therapeutic outcomes, and reduced healthcare costs <sup><a href="#ref-aldirSingletabletRegimensHIV2014" role="doc-biblioref">553</a></sup>.

![**Timeline of ART drugs FDA approvals.**  
Colored by drug type: Nucleoside Reverse transcriptase inhibitors (NRTI), Non-Nucleoside Reverse transcriptase inhibitors (NNRTI), Protease Inhibitors (PI), Integrase inhibitors (INSTI), Entry Inhibitors (EI) and pharmacokinetic enhancers (PE). Fixed Dose Combination (FDC) single pill regimens are also shown.  
* RPV is often also used as a pharmacokinetic enhancer in combination with other drugs.  
✝ These drugs are no longer approved by the FDA or no longer recommended as first line regiment treatment.  
Information collected from <https://hivinfo.nih.gov/understanding-hiv/fact-sheets/fda-approved-hiv-medicines>, <https://hivinfo.nih.gov/understanding-hiv/infographics/fda-approval-hiv-medicines> and <https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm>.  
See also Table \@ref(tab:tableDrugs).](https://thesis.lucblassel.com/figures/HIV-Intro/complete.png)

Figure 5.3: **Timeline of ART drugs FDA approvals.**  
Colored by drug type: Nucleoside Reverse transcriptase inhibitors (NRTI), Non-Nucleoside Reverse transcriptase inhibitors (NNRTI), Protease Inhibitors (PI), Integrase inhibitors (INSTI), Entry Inhibitors (EI) and pharmacokinetic enhancers (PE). Fixed Dose Combination (FDC) single pill regimens are also shown.  
\* RPV is often also used as a pharmacokinetic enhancer in combination with other drugs.  
✝ These drugs are no longer approved by the FDA or no longer recommended as first line regiment treatment.  
Information collected from [https://hivinfo.nih.gov/understanding-hiv/fact-sheets/fda-approved-hiv-medicines](https://hivinfo.nih.gov/understanding-hiv/fact-sheets/fda-approved-hiv-medicines), [https://hivinfo.nih.gov/understanding-hiv/infographics/fda-approval-hiv-medicines](https://hivinfo.nih.gov/understanding-hiv/infographics/fda-approval-hiv-medicines) and [https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm](https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm).  
See also Table [B.1](https://thesis.lucblassel.com/HIV-intro-appendix.html#tab:tableDrugs).

Most recently, some studies explored using some of these single pill regimens (such as Truvada, c.f. Table [B.1](https://thesis.lucblassel.com/HIV-intro-appendix.html#tab:tableDrugs)) as prophylactics, called Pre-exposure prophylaxis (PrEP). Putting uninfected but at risk populations on ART, before any known exposure, has been shown to effectively lower the risk of infection <sup><a href="#ref-grantPreexposureChemoprophylaxisHIV2010" role="doc-biblioref">554</a> – <a href="#ref-buchbinderPreexposureProphylaxisPromise2011" role="doc-biblioref">556</a></sup>. When adherence is maintained, this risk reduction has been estimated to be between 44% and 100% <sup><a href="#ref-riddellHIVPreexposureProphylaxis2018" role="doc-biblioref">557</a></sup>. As of 2022, Truvada is the only authorized drug for PrEP in Europe <sup><a href="#ref-emaTruvada2018" role="doc-biblioref">558</a></sup>. Descovy and Apretude are also authorized for PrEP in the USA <sup><a href="#ref-PrEPPrEPHIV2022" role="doc-biblioref">559</a></sup>.

All of these drugs are widely used and are by now very well studied, therefore detailed guidelines on all the aspects of ART; when to start, which drugs to use, when to change drugs; are issued and updated regularly by practitioners <sup><a href="#ref-zolopaEvolutionHIVTreatment2010" role="doc-biblioref">560</a></sup> and global instances <sup><a href="#ref-worldhealthorganizationConsolidatedGuidelinesHIV2021" role="doc-biblioref">561</a></sup> alike.

### 5.3.2 Main mechanisms of viral proteins, antiretroviral drugs and associated resistance.

Each ART drug targets a specific protein. Most of them target one of the three *pol* proteins: RT, PR and IN. The structure of these proteins is inherently linked to their function, and as such is essential to take into account when developing ART. Similarly, the structure of these proteins is very important when studying the resistance mechanisms developed by the virus <sup><a href="#ref-ammaranondMechanismHIVAntiretroviral2012" role="doc-biblioref">562</a>,<a href="#ref-clavelHIVDrugResistance2004" role="doc-biblioref">563</a></sup>. In this section we will go over the main structural elements and how they relate to treatment and resistance, for RT, IN and PR.

#### 5.3.2.1 Reverse transcriptase

The reverse transcriptase protein is the most targeted protein, in number of ART drugs (*c.f.* Figure [5.3](https://thesis.lucblassel.com/viruses-hiv-and-drug-resistance.html#fig:timeline) and Table [B.1](https://thesis.lucblassel.com/HIV-intro-appendix.html#tab:tableDrugs)). The mature protein is formed of two subunits: p51 and p66. These two subunits are translated from the same section of the *pol* gene, and have the same amino acid sequence, but p51 is cleaved and is shorter than p66. The p66 subunit contains the active sites of RT whereas p51 plays a mainly structural role.

The p66 sububit can be separated into 5 domains <sup><a href="#ref-sarafianosStructureFunctionHIV12009" role="doc-biblioref">564</a></sup>. The “fingers”, “palm”, and “thumb” domains are linked together and folded to form a canal through which the RNA template and newly synthesized viral DNA can pass through. The polymerase active site, responsible for incorporating nucleotides to the viral DNA molecule, is situated in the “palm” domain at the bottom of the canal. The “RNase” domain of RT contains a secondary active site responsible for cleaving the viral RNA template from the viral DNA so that the RT can fill out the complementary strand of viral DNA before integration into the host genome. The final “connection” domain is simply a link between the “RNase” and the “thumb” domains. A three dimensional view of RT with these domains highlighted can be seen in Figure [5.4](https://thesis.lucblassel.com/viruses-hiv-and-drug-resistance.html#fig:rtStruct).

![**3D structure of HIV-1 Reverse-transcriptase.**  
The different domains of the p66 subunit are labeled and shown in different shades of blue and green. The structural p51 subunit is shown in orange. The RNA template is shown in dark gray and the newly synthesized DNA strand in light gray. The polymerase active site is shown in red, although mostly hidden by the RNA template. The 3D visualization was produced with Illustrate [@goodsellIllustrateSoftwareBiomolecular2019] using the [2hmi](https://www.rcsb.org/structure/2HMI) PDB structure.](https://thesis.lucblassel.com/figures/HIV-Intro/rt.png)

Figure 5.4: **3D structure of HIV-1 Reverse-transcriptase.**  
The different domains of the p66 subunit are labeled and shown in different shades of blue and green. The structural p51 subunit is shown in orange. The RNA template is shown in dark gray and the newly synthesized DNA strand in light gray. The polymerase active site is shown in red, although mostly hidden by the RNA template. The 3D visualization was produced with Illustrate <sup><a href="#ref-goodsellIllustrateSoftwareBiomolecular2019" role="doc-biblioref">565</a></sup> using the [2hmi](https://www.rcsb.org/structure/2HMI) PDB structure.

Reverse Transcriptase inhibitors can be separated into two classes: Nucleoside RTIs (NRTIs) and Non-Nucleoside RTIs (NNRTIs). They inhibit the action of RT in two disctinct manners:

- NRTIs are analogues of free nucleotides in the host cell. They competitively inhibit RT and can be used to elongate the viral DNA chain. Once an NRTI is incorporated, further elongation of the DNA molecule is impossible and the viral DNA cannot be synthesized anymore. This is similar to the chain terminating nucleotides introduced in Section [1.2](https://thesis.lucblassel.com/what-is-sequence-data.html#obtaining-sequence-data).
- NNRTIs bind to a specific region of the p51 subunit: the Non Nucleoside Inhibitor Binding Pocket (NNIBP) (A view of RT with the NNIBP visible is shown in Figure [6.4](https://thesis.lucblassel.com/HIV-paper.html#fig:figStructure)). This pocket, although it is on the p51 subunit is spatially situated very close to the polymerase active site. NNRTIs bind to the NNIBP to change the conformation of the active site, lowering its flexibility <sup><a href="#ref-esnoufUniqueFeaturesStructure1997" role="doc-biblioref">566</a></sup>, and thus non-competitively inhibiting the action of RT.

Research has been conducted into inhibition of the RNase active site of RT <sup><a href="#ref-hangActivityIsolatedHIV2004" role="doc-biblioref">567</a>,<a href="#ref-klumppRecentProgressDesign2006" role="doc-biblioref">568</a></sup> which could also inhibit the action of RT. There is, however, to this day, no approved treatment that inhibits the RNase action of RT.

Drug resistance mutations (DRMs) that arise in HIV from the selective pressures resulting from RTI exposure can similarly be grouped into two categories: NRTI and NNRTI resistance mutations.

NRTI resistance mutations can further be subcategorized into two groups <sup><a href="#ref-menendez-ariasMechanismsResistanceNucleoside2008" role="doc-biblioref">569</a>,<a href="#ref-sluis-cremerMolecularMechanismsHIV12000" role="doc-biblioref">570</a></sup>. The first type of NRTI resistance mutations are mutations that prevent the incorporation of NRTIs into the viral DNA molecule. M184V and M184I, indicating the replacement, at site number 184, of a Methionine by a Valine or an Isoleucine respectively, are very common NRTI resistance mutations. These V and I amino acids have a different structure than the original M, interfering with the incorporation of lamiduvine (3TC) but not dNTP <sup><a href="#ref-sarafianosLamivudine3TCResistance1999" role="doc-biblioref">571</a></sup>. The second type of mutation, allows RT to remove an incorporated NRTI from the viral DNA to resume synthesis. Thymidine Analog Mutations (TAMs), M41L, D67N, K70R, L210W, T215Y/F and K219Q/E confer resistance to azidothymidine (AZT) through this mechanism <sup><a href="#ref-meyerMechanismAZTResistance1999" role="doc-biblioref">572</a>,<a href="#ref-boyerSelectiveExcisionAZTMP2001" role="doc-biblioref">573</a></sup>.

Similarly, NNRTI resistance mutations work via several different mechanisms <sup><a href="#ref-deeksNonnucleosideReverseTranscriptase2001" role="doc-biblioref">574</a>,<a href="#ref-renStructuralBasisDrug2008" role="doc-biblioref">575</a></sup>. Some NNRTI resistance mutations, like Y181C, lower the affinity of the NNIBP to NNRTIs preventing binding of drugs to RT. Others, like K103N change the conformation of the p51 subunit, making the NNIBP disappear. NNRTI resistance mutations are particularly dangerous because they often confer cross-resistance to multiple NNRTIs without affecting the polymerase action very much <sup><a href="#ref-ammaranondMechanismHIVAntiretroviral2012" role="doc-biblioref">562</a></sup>, giving rise to viruses that are both fit and highly resistant. This is contrast to NRTI resistance mutations that generally incur a fitness cost for the virus, lowering its efficacy <sup><a href="#ref-lloydHighCostFidelity2014" role="doc-biblioref">576</a></sup>.

#### 5.3.2.2 Protease

The Protease protein, also a major drug target for ART, cleaves the *gag* and *pol* polyproteins in order to produce functional viral proteins, essential to replication. It has a symmetric, dimeric, structure. That is to say: it is composed of two identical chains of amino acids <sup><a href="#ref-pearlStructuralModelRetroviral1987" role="doc-biblioref">577</a>,<a href="#ref-gulnikHIVProteaseEnzyme2000" role="doc-biblioref">578</a></sup>. A structural view of PR is shown in Figure [5.5](https://thesis.lucblassel.com/viruses-hiv-and-drug-resistance.html#fig:prStruct).

These two chains are folded in order to create a “tunnel” through which the polyproteins enter. In the middle of this “tunnel”, at the bottom, is the active site. The active site is composed of two Aspartate residues, one on each chain. Using water, they can provoke a chemical reaction that cleaves the polyprotein at a specific position <sup><a href="#ref-silvaInhibitionCatalyticMechanism1996" role="doc-biblioref">579</a></sup>.

The roof of the “tunnel” is formed by the flaps, a flexible region from each of the two chains that can open or close the “tunnel” <sup><a href="#ref-hornakHIV1ProteaseFlaps2006" role="doc-biblioref">580</a></sup>. These flaps most likely control the access of polyproteins to the active site <sup><a href="#ref-freedbergRapidStructuralFluctuations2002" role="doc-biblioref">581</a>,<a href="#ref-yuStructuralInsightsHIV12017" role="doc-biblioref">582</a></sup>.

![**3D structure of HIV-1 Protease.**  
The two identical chains are colored in orange and blue shades respectively. The flexible flaps form the the "roof" of a tunnel, at the bottom of which is the active site: 2 Asp residues, one on each chain. The 3D visualization was produced with Illustrate [@goodsellIllustrateSoftwareBiomolecular2019] using the [2p3b](https://www.rcsb.org/structure/2P3B) PDB structure.](https://thesis.lucblassel.com/figures/HIV-Intro/pr.png)

Figure 5.5: **3D structure of HIV-1 Protease.**  
The two identical chains are colored in orange and blue shades respectively. The flexible flaps form the the “roof” of a tunnel, at the bottom of which is the active site: 2 Asp residues, one on each chain. The 3D visualization was produced with Illustrate <sup><a href="#ref-goodsellIllustrateSoftwareBiomolecular2019" role="doc-biblioref">565</a></sup> using the [2p3b](https://www.rcsb.org/structure/2P3B) PDB structure.

All the approved Protease Inhibitors (PIs) share a similar mode of action. Each PI binds to the active site of the PR, denying access to the “tunnel” for polyproteins, and stopping the catalytic action of PR <sup><a href="#ref-robertsRationalDesignPeptideBased1990" role="doc-biblioref">583</a>,<a href="#ref-lvHIVProteaseInhibitors2015" role="doc-biblioref">584</a></sup>. Tipranavir, one of the more recent PIs, also binds with the flaps <sup><a href="#ref-lvHIVProteaseInhibitors2015" role="doc-biblioref">584</a></sup>.

According to Prabu-Jeyabalan *et al.*, PR does not recognize the specific sequence of the polyprotein cleavage site but rather its shape <sup><a href="#ref-prabu-jeyabalanSubstrateShapeDetermines2002" role="doc-biblioref">585</a></sup>. They proposed an inhibitor based on the shape of all polyproteins combined, which establishes more bonds with PR, making it supposedly more efficient <sup><a href="#ref-prabu-jeyabalanSubstrateEnvelopeDrug2006" role="doc-biblioref">586</a></sup> than current approved PIs.

As is the case with RTIs, when under selective pressure due to PIs, the virus tends to develop PI associated DRMs. Most PI resistance mutations result in an enlarged “tunnel”. This tends to lower the affinity of the PIs to the active site, but also the affinity of polyproteins, lowering the fitness of the virus significantly <sup><a href="#ref-wensingFifteenYearsHIV2010" role="doc-biblioref">541</a></sup>. In addition, some mutations on the *gag* polyprotein seem to lower the efficacy of PIs, although the underlying mechanism is not well known <sup><a href="#ref-wensingFifteenYearsHIV2010" role="doc-biblioref">541</a></sup>.

Some mutations in the flaps of PR have also been shown to confer PI resistance. It seems likely that these mutations change conformation of the flaps, opening them and leading to the release of inhibitors from the active site <sup><a href="#ref-kurtyilmazImprovingViralProtease2016" role="doc-biblioref">587</a></sup>.

#### 5.3.2.3 Integrase

The integrase protein is the third major anti-retroviral drug target. It is responsible for integrating the viral DNA into the host genome. IN is a tetramer composed of four identical amino acid chains <sup><a href="#ref-chiuStructureFunctionHIV12004" role="doc-biblioref">588</a>,<a href="#ref-espositoHIVIntegraseStructure1999" role="doc-biblioref">589</a></sup>. Each of these chains contain three domains linked together by flexible linker sequences: the N-terminal domain, the catalytic core and the C-terminal domain. In each tetramer, two chains provide the active site for the integration reaction while the other two have a mostly structural role. It is probable that the N-terminal domain, which is very conserved, is necessary for stable tetramerization of IN monomers <sup><a href="#ref-delelisIntegraseIntegrationBiochemical2008" role="doc-biblioref">590</a></sup>. This tetrameric structure is shown in Figure [5.6](https://thesis.lucblassel.com/viruses-hiv-and-drug-resistance.html#fig:inStruct).

![**3D structure of an Integrase.**  
This Integrase tetramer is binded with viral (red) and host (orange) DNA, linked to the two light blue functional subunits via the C-terminal domain. The active site formed by the the catalytic cores of the two functional subunits *(not visible in this representation)*, is where the strand transfer reaction will take place. The two dark blue IN subunits have a structural role. 
This figure was adapted from the PDB 101 molecule of the month Integrase entry by David S. Goodsell and the RCSB PDB ([pdb101.rcsb.org/motm/135](https://pdb101.rcsb.org/motm/135)) with a CC By 4.0 license. ](https://thesis.lucblassel.com/figures/HIV-Intro/in.png)

Figure 5.6: **3D structure of an Integrase.**  
This Integrase tetramer is binded with viral (red) and host (orange) DNA, linked to the two light blue functional subunits via the C-terminal domain. The active site formed by the the catalytic cores of the two functional subunits *(not visible in this representation)*, is where the strand transfer reaction will take place. The two dark blue IN subunits have a structural role. This figure was adapted from the PDB 101 molecule of the month Integrase entry by David S. Goodsell and the RCSB PDB ([pdb101.rcsb.org/motm/135](https://pdb101.rcsb.org/motm/135)) with a CC By 4.0 license.

Several steps are needed in order to integrate the viral DNA with the host genome <sup><a href="#ref-maertensStructureFunctionRetroviral2022" role="doc-biblioref">591</a></sup>. First, IN binds to the both ends of the viral DNA, using the C-terminal domains, forming a closed loop. Secondly, both ends of the viral DNA molecule are then prepared for integration by the catalytic core. Third, the host DNA is captured with C-terminal domains. Then, the strand-transfer is done within the catalytic core: the host DNA is cut in two places and a single strand from each end of the viral DNA are attached to these two breakpoints. Finally, the IN tetramer detaches from the linked molecules and the final steps necessary to create a single hybrid DNA molecule are done by the host cellular machinery. A graphical representation of this process can be found in Figure 1 of Maertens *et al.* (2022) <sup><a href="#ref-maertensStructureFunctionRetroviral2022" role="doc-biblioref">591</a></sup>.

Integrase Strand Transfer Inhibitors (INSTIs), as their name indicates, block the strand transfer reaction. They achieve this by strongly binding to the active site of the IN tetramer after it has formed a complex with the viral DNA <sup><a href="#ref-maertensStructureFunctionRetroviral2022" role="doc-biblioref">591</a>,<a href="#ref-pommierIntegraseInhibitorsTreat2005" role="doc-biblioref">592</a></sup>. In doing so, INSTIs prevent the IN / viral DNA complex from binding to the host DNA, effectively preventing strand transfer.

In the presence of INSTIs during therapy, once more, the HIV virus develops resistance mutations over time. These mutations all lower affinity of IN to INSTIs, preventing bonding <sup><a href="#ref-maertensStructureFunctionRetroviral2022" role="doc-biblioref">591</a>,<a href="#ref-blancoHIV1IntegraseInhibitor2011" role="doc-biblioref">593</a></sup>. Since most INSTIs behave similarly, this means that cross-resistance to INSTIs is quite common for INSTI DRMs <sup><a href="#ref-blancoHIV1IntegraseInhibitor2011" role="doc-biblioref">593</a>,<a href="#ref-gerettiEmergingPatternsImplications2012" role="doc-biblioref">594</a></sup>. Again, these mutations tend to lower the overall viral fitness necessitating secondary compensatory mutations to restore fitness <sup><a href="#ref-blancoHIV1IntegraseInhibitor2011" role="doc-biblioref">593</a>,<a href="#ref-gerettiEmergingPatternsImplications2012" role="doc-biblioref">594</a></sup>.

#### 5.3.2.4 Other drug targets

For now, resistance has not been observed for novel drugs like entry inhibitors. This might be because the genetic barrier to resistance is higher and not enough time has passed since their introduction for resistance to emerge.

For all the other drug targets however, as stated earlier in this section, resistance is documented and problematic. Resistance has even been detected for PrEP which is prophylactic <sup><a href="#ref-knoxMultidrugResistantHIV1Infection2017" role="doc-biblioref">595</a>,<a href="#ref-hurtPreexposureProphylaxisAntiretroviral2011" role="doc-biblioref">596</a></sup>. This seems to be rare however, and mostly due to unknown pre-treatment HIV infections <sup><a href="#ref-gibasDrugResistanceHIV2019" role="doc-biblioref">597</a></sup>.

### 5.3.3 Consequences of resistance on global health

HIV resistance to ART drugs is problematic from a global health perspective. Indeed, circulation of resistant strains of HIV within populations can lead to treatment-naive individuals that will not respond well to treatment.

More concerning, is the fact that transmission of resistant strains of HIV between treatment-naive individuals is the main mode of resistance transmission in the UK <sup><a href="#ref-mouradPhylotypebasedAnalysisHighlights2015" role="doc-biblioref">598</a>,<a href="#ref-hueDemonstrationSustainedDrugResistant2009" role="doc-biblioref">599</a></sup> and Switzerland <sup><a href="#ref-drescherTreatmentNaiveIndividualsAre2014" role="doc-biblioref">600</a></sup>. This treatment-naive to treatment-naive transmission is particularly insidious since it can go undetected and creates long lasting drug resistant strain reservoirs in the treatment-naive population. This of course is dangerous since some infected individuals might experience poor therapeutic outcomes and even treatment failure when administered first line regimens <sup><a href="#ref-boermaHighLevelsPretreatment2016" role="doc-biblioref">601</a></sup>. To avoid this, genotypic resistance testing has become standard practice when choosing the therapeutic strategy in high-income countries, but more effort must be done to make resistance testing less expensive and more cost-efficient in lower and middle income countries <sup><a href="#ref-clutterHIV1DrugResistance2016" role="doc-biblioref">602</a></sup>.

Although the transmitted drug resistance described above is problematic, a large portion of DRMs incur a fitness cost for the resistant strain <sup><a href="#ref-kuhnertQuantifyingFitnessCost2018" role="doc-biblioref">603</a>,<a href="#ref-mespledeViralFitnessCost2013" role="doc-biblioref">604</a></sup>. This means that, although they are selected when exposed to the evolutionary pressure of ART, when the treatment is interrupted there is another pressure leading these costly mutations to disappear. This reversion is commonly observed after interruption of treatment, however the median reversion times vary widely from 1 to 13 years <sup><a href="#ref-castroPersistenceHIV1Transmitted2013" role="doc-biblioref">605</a></sup> depending on the severity of the fitness loss and type of mutation. This means that, although reversion can possibly lead to loss of resistance, this can potentially take a long time and possibly longer than the treatment interruption.

In practice, it is therefore very important to keep an eye on all drug resistance mutations, their population dynamics, and spread as well as their presence or absence in a particular strain before starting treatment.

### 5.3.4 Finding DRMs

Finding and categorizing mutations as DRMs is an important task in light of the public health implications mentioned in Section [5.3.3](https://thesis.lucblassel.com/viruses-hiv-and-drug-resistance.html#consequences-of-resistance-on-global-health). As such, this is an active part of the HIV research field.

The most important thing needed in order to study DRMs is, of course, viral sequences. To facilitate the search for DRMs, several sequence databases exist. Sequences are often linked to metadata related to the treatment status of the patient from which the sequence was obtained. This metadata can be quite variable: from a coarse level binary indicator of treatment to a finely detailed list of all treatments received and associated phenotypic measurements like viral load.

Databases like the UK-CHIC <sup><a href="#ref-ukchicsteeringcommitteeCreationLargeUKbased2004" role="doc-biblioref">607</a></sup>, UK HIV drug resistance database ([https://www.hivrdb.org.uk/](https://www.hivrdb.org.uk/)) and Swiss cohort study ([https://www.shcs.ch/](https://www.shcs.ch/)) host sequences on a national level, although access can be granted to international researchers. Other databases like the PANGEA database <sup><a href="#ref-abeler-dornerPANGEAHIVPhylogeneticsNetworks2019" role="doc-biblioref">608</a></sup> host sequences from multiple countries in sub-Saharan Africa. The Stanford HIV drug resistance database ([https://hivdb.stanford.edu/](https://hivdb.stanford.edu/)) hosts HIV sequences with some phenotypic data <sup><a href="#ref-rheeHumanImmunodeficiencyVirus2003" role="doc-biblioref">33</a>,<a href="#ref-shaferRationaleUsesPublic2006" role="doc-biblioref">609</a></sup>. Finally some database only host sequences, such as the Los Alamos HIV sequence database ([http://www.hiv.lanl.gov/](http://www.hiv.lanl.gov/)). However, with few specific treatment or resistance related metadata <sup><a href="#ref-kuikenHIVSequenceDatabases2003" role="doc-biblioref">610</a></sup>, these have less direct applicability to the DRM search task.

Some databases, like the Stanford HIV resistance database also store specific knowledge about known resistance mutations, keeping and regularly updating lists of clinically important DRMs as well as their impact on ART <sup><a href="#ref-wensing2019UpdateDrug2019" role="doc-biblioref">611</a>,<a href="#ref-clarkMutationsRetroviralGenes2007" role="doc-biblioref">612</a></sup>. Additionally, Stanford also offers tools for clinicians to do genotypic resistance testing with interpretable results <sup><a href="#ref-liuWebResourcesHIV2006" role="doc-biblioref">613</a></sup>.

The first step of mutations discovery is usually some kind of statistical association analysis <sup><a href="#ref-wensing2019UpdateDrug2019" role="doc-biblioref">611</a>,<a href="#ref-johnsonUpdateDrugResistance2016" role="doc-biblioref">614</a></sup> where the association between treatment status (coarse of fine grained) and specific mutations is statistically tested. This is usually done with Fisher association tests <sup><a href="#ref-villabona-arenasIndepthAnalysisHIV12016" role="doc-biblioref">615</a>,<a href="#ref-shulmanGeneticCorrelatesEfavirenz2004" role="doc-biblioref">616</a></sup> or correlation testing with the Spearman correlation <sup><a href="#ref-millerGenotypicPhenotypicPredictors2004" role="doc-biblioref">617</a></sup>. This results in a list of mutations that are significantly associated with a given treatment and corresponding p-values.

Since, on a given sequence dataset, several mutations are usually tested at once, this can lead to inflated false positives <sup><a href="#ref-brownMethodsCorrectingMultiple1997" role="doc-biblioref">618</a></sup> and spurious associations <sup><a href="#ref-austinTestingMultipleStatistical2006" role="doc-biblioref">619</a></sup>. Fortunately, this is a well studied problem and many methods exist to control this effect by controlling the Familywise Error Rate (FWER) *e.g.* with the Bonferroni procedure <sup><a href="#ref-hochbergMultipleComparisonProcedures1987" role="doc-biblioref">620</a></sup>, or the False Discovery Rate (FDR) *e.g.* with the Benjamini-Hochberg procedure <sup><a href="#ref-benjaminiControllingFalseDiscovery1995" role="doc-biblioref">621</a></sup>. These methods are often applied when testing for resistance association <sup><a href="#ref-villabona-arenasIndepthAnalysisHIV12016" role="doc-biblioref">615</a>,<a href="#ref-gonzalesExtendedSpectrumHIV12003" role="doc-biblioref">622</a>,<a href="#ref-seoigheModelDirectionalSelection2007" role="doc-biblioref">623</a></sup>. However, these correction methods are a double-edged sword, some of them can be very conservative and lead to falsely rejecting true associations <sup><a href="#ref-shamStatisticalPowerSignificance2014" role="doc-biblioref">624</a></sup>. In some studies on resistance, phylogenetic correlation between the sequences is also accounted for <sup><a href="#ref-alizonPhylogeneticApproachReveals2010" role="doc-biblioref">625</a>,<a href="#ref-flynnDeepSequencingProtease2015" role="doc-biblioref">626</a></sup>.

Statistical testing on treatment status, while informative, can only associate a mutation with a treatment. In order to actually validate whether a mutation causes resistance or not, biological analyses are needed <sup><a href="#ref-wensing2019UpdateDrug2019" role="doc-biblioref">611</a>,<a href="#ref-johnsonUpdateDrugResistance2016" role="doc-biblioref">614</a></sup>. The easiest of these are *in vitro* analyses where live viruses are subjected to a phenotypical assay. These assays measure the susceptibility of HIV viruses to a wide array of drugs, which can then be statistically associated with genetic traits like specific mutations. These assays like phenosense <sup><a href="#ref-petropoulosNovelPhenotypicDrug2000" role="doc-biblioref">627</a></sup> or antivirogram <sup><a href="#ref-hertogsRapidMethodSimultaneous1998" role="doc-biblioref">628</a></sup> are widely used <sup><a href="#ref-heilek-snyderRoleHIVPhenotypic2002" role="doc-biblioref">629</a> – <a href="#ref-gartlandSusceptibilityGlobalHIV12021" role="doc-biblioref">631</a></sup>. Viruses can be obtained from clinical isolates <sup><a href="#ref-masquelierGenotypicPhenotypicResistance2001" role="doc-biblioref">632</a></sup>, or viruses with specific mutations can be manufactured with site directed mutagenesis <sup><a href="#ref-larderMultipleMutationsHIV11989" role="doc-biblioref">633</a>,<a href="#ref-devreeseResistanceHumanImmunodeficiency1992" role="doc-biblioref">634</a></sup>. *In vivo* studies can be conducted by sequencing viruses from patients failing ART, following over time and studying the association between their treatment response and HIV genetics <sup><a href="#ref-tambuyzerEffectMutationsPosition2011" role="doc-biblioref">635</a>,<a href="#ref-katzensteinPhenotypicSusceptibilityVirological2003" role="doc-biblioref">636</a></sup>.

More recently, as sequence database grow bigger and bigger *(The UK-CHIC database contains more than 80,000 HIV sequences with treatment status)*, methods based on statistical and machine learning are being used to study resistance. Most approaches rely on training models to predict some type of resistance: either classifying sequences as resistant or not <sup><a href="#ref-steinerDrugResistancePrediction2020" role="doc-biblioref">331</a>,<a href="#ref-blasselUsingMachineLearning2021" role="doc-biblioref">637</a></sup> of predicting a phenotypic response like fold resistance compared to wild type <sup><a href="#ref-sheikamamuddyImprovingFoldResistance2017" role="doc-biblioref">638</a></sup>. Initial approaches were mainly designed for clinical testing, rather than new DRM search, and distributed via web services <sup><a href="#ref-beerenwinkelGeno2phenoInterpretingGenotypic2001" role="doc-biblioref">639</a>,<a href="#ref-riemenschneiderSHIVAWebApplication2016" role="doc-biblioref">640</a></sup>.

Initially these approaches were based on models like decision trees <sup><a href="#ref-beerenwinkelDiversityComplexityHIV12002" role="doc-biblioref">641</a></sup>, SVMs <sup><a href="#ref-beerenwinkelGeno2phenoInterpretingGenotypic2001" role="doc-biblioref">639</a></sup> or logistic regression <sup><a href="#ref-heiderMultilabelClassificationExploiting2013" role="doc-biblioref">642</a></sup>. Over time the use of more complex models such as neural networks has increased, with increased prediction accuracy <sup><a href="#ref-sheikamamuddyImprovingFoldResistance2017" role="doc-biblioref">638</a></sup>.

By analyzing the important features used by trained models to predict resistance, it is possible to find features corresponding to mutations, that are useful for predicting, and therefore likely associated with, drug resistance (see Chapter [6](https://thesis.lucblassel.com/HIV-paper.html#HIV-paper)). With the improvement in methods to interpret and extract features from complex models such as deep neural networks, this approach has been used with deep learning models <sup><a href="#ref-steinerDrugResistancePrediction2020" role="doc-biblioref">331</a></sup>. This novel way of finding resistance associated mutations has the potential to uncover complex mutational effects that simple association testing cannot.

## 5.4 Conclusion

Viruses are surprisingly complex in light of their apparent simplicity. They are ubiquitous and present an extreme diversity. Whether they are pathogenic or not, the role of viruses in a myriad of processes and niches make them interesting and important to study. The sequences of these viruses, although small can be very useful for evolutionary as well as clinical analyses.

Although the study of viruses as a whole is very useful, HIV is particularly important to study. The impact of the HIV pandemic on global health has been severe, both in Lower and Higher income countries. It is therefore paramount to fully understand the underlying mechanisms and evolutionary adaptations of this virus. Its high mutation rate allows it to quickly explore evolutionary alternatives when exposed to drugs, making anti HIV therapy a complex endeavor.

Fortunately, with large scale sequencing efforts it is possible to study and track these evolutionary adaptations to treatments. This allows us to adapt therapeutic strategies as well as develop new compounds and approaches. In this context, studying and finding the virus’s mutational processes is paramount. This is especially important when studying resistance to RTIs as they form the backbone of first line regimen combination therapies, and are the most common type of anti-HIV drug. This process is made easier by the large scale sequence repositories now available, and the usage of machine and statistical learning to leverage that data.

### References

33.

Rhee, S.-Y. *et al.* [Human immunodeficiency virus reverse transcriptase and protease sequence database](https://doi.org/10.1093/nar/gkg100). *Nucleic Acids Res* **31**, 298–303 (2003).

331.

Steiner, M. C., Gibson, K. M. & Crandall, K. A. [Drug Resistance Prediction Using Deep Learning Techniques on HIV-1 Sequence Data](https://doi.org/10.3390/v12050560). *Viruses* **12**, 560 (2020).

424.

Lwoff, A. [The concept of virus](https://doi.org/10.1099/00221287-17-2-239). *J Gen Microbiol* **17**, 239–253 (1957).

425.

Minor, P. D. Viruses. in *eLS* (John Wiley & Sons, Ltd, 2014). doi:[10.1002/9780470015902.a0000441.pub3](https://doi.org/10.1002/9780470015902.a0000441.pub3).

426.

Stapleton, J. T., Foung, S., Muerhoff, A. S., Bukh, J. & Simmonds, P. [The GB viruses: A review and proposed classification of GBV-A, GBV-C (HGV), and GBV-D in genus Pegivirus within the family Flaviviridae](https://doi.org/10.1099/vir.0.027490-0). *J Gen Virol* **92**, 233–246 (2011).

427.

Yamamoto, N. *et al.* [Characterization of a non-pathogenic H5N1 influenza virus isolated from a migratory duck flying from Siberia in Hokkaido, Japan, in October 2009](https://doi.org/10.1186/1743-422x-8-65). *Virology Journal* **8**, 65 (2011).

428.

Shi, M. *et al.* [The evolutionary history of vertebrate RNA viruses](https://doi.org/10.1038/s41586-018-0012-7). *Nature* **556**, 197–202 (2018).

429.

Adams, J. R. & Bonami, J.-R. *Atlas of Invertebrate Viruses*. (CRC Press, 2017). doi:[10.1201/9781315149929](https://doi.org/10.1201/9781315149929).

430.

Lefeuvre, P. *et al.* [Evolution and ecology of plant viruses](https://doi.org/10.1038/s41579-019-0232-3). *Nat Rev Microbiol* **17**, 632–644 (2019).

431.

Wang, A. L. & Wang, C. C. [Viruses of parasitic protozoa](https://doi.org/10.1016/0169-4758\(91\)90198-w). *Parasitology Today* **7**, 76–80 (1991).

432.

Fermin, G., Mazumdar-Leighton, S. & Tennant, P. Viruses of prokaryotes, protozoa, fungi, and chromista. in *Viruses: Molecular Biology, Host Interactions, and Applications to Biotechnology* 217 (Academic Press, 2018). doi:[10.1016/B978-0-12-811257-1.00009-7](https://doi.org/10.1016/B978-0-12-811257-1.00009-7).

433.

Sutela, S., Poimala, A. & Vainio, E. J. [Viruses of fungi and oomycetes in the soil environment](https://doi.org/10.1093/femsec/fiz119). *FEMS Microbiology Ecology* **95**, fiz119 (2019).

434.

Twort, F. W. [An Investigation On The Nature Of Ultra-microscopic Viruses.](https://doi.org/10.1016/s0140-6736\(01\)20383-3) *The Lancet* **186**, 1241–1243 (1915).

435.

Delbrock, M. [Bacterial Viruses or Bacteriophages](https://doi.org/10.1111/j.1469-185X.1946.tb00451.x). *Biological Reviews* **21**, 30–40 (1946).

436.

Clark, J. R. & March, J. B. [Bacterial viruses as human vaccines?](https://doi.org/10.1586/14760584.3.4.463) *Expert Review of Vaccines* **3**, 463–476 (2004).

437.

van Kan-Davelaar, H. E., van Hest, J. C. M., Cornelissen, J. J. L. M. & Koay, M. S. T. [Using viruses as nanomedicines](https://doi.org/10.1111/bph.12662). *British Journal of Pharmacology* **171**, 4001–4009 (2014).

438.

Prangishvili, D., Basta, T., Garrett, R. A. & Krupovic, M. Viruses of the Archaea. in *eLS* 1–9 (John Wiley & Sons, Ltd, 2016). doi:[10.1002/9780470015902.a0000774.pub3](https://doi.org/10.1002/9780470015902.a0000774.pub3).

439.

Prangishvili, D., Forterre, P. & Garrett, R. A. [Viruses of the Archaea: A unifying view](https://doi.org/10.1038/nrmicro1527). *Nat Rev Microbiol* **4**, 837–848 (2006).

440.

Francki, R. I. B. [Plant virus satellites](https://10.0.4.122/annurev.mi.39.100185.001055). *Annual Review Of Microbiology* (1985).

441.

Xu, P. & Roossinck, M. J. Plant Virus Satellites. in *eLS* (John Wiley & Sons, Ltd, 2011). doi:[10.1002/9780470015902.a0000771.pub2](https://doi.org/10.1002/9780470015902.a0000771.pub2).

442.

Lai, M. M. [The molecular biology of hepatitis delta virus](https://doi.org/10.1146/annurev.bi.64.070195.001355). *Annu Rev Biochem* **64**, 259–286 (1995).

443.

Hughes, S. A., Wedemeyer, H. & Harrison, P. M. [Hepatitis delta virus](https://doi.org/10.1016/s0140-6736\(10\)61931-9). *The Lancet* **378**, 73–85 (2011).

444.

Desnues, C., Boyer, M. & Raoult, D. [Chapter 3 - Sputnik, a Virophage Infecting the Viral Domain of Life](https://doi.org/10.1016/b978-0-12-394621-8.00013-3). in *Advances in Virus Research* (eds. Łobocka, M. & Szybalski, W. T.) vol. 82 63–89 (Academic Press, 2012).

445.

Gaia, M. *et al.* [Zamilon, a Novel Virophage with Mimiviridae Host Specificity](https://doi.org/10.1371/journal.pone.0094923). *Plos One* **9**, e94923 (2014).

446.

Edgar, R. C. *et al.* [Petabase-scale sequence alignment catalyses viral discovery](https://doi.org/10.1038/s41586-021-04332-2). *Nature* **602**, 142–147 (2022).

447.

Nasir, A., Romero-Severson, E. & Claverie, J.-M. [Investigating the Concept and Origin of Viruses](https://doi.org/10.1016/j.tim.2020.08.003). *Trends in Microbiology* **28**, 959–967 (2020).

448.

Forterre, P. & Prangishvili, D. [The origin of viruses](https://doi.org/10.1016/j.resmic.2009.07.008). *Research in Microbiology* **160**, 466–472 (2009).

449.

Forterre, P. [The origin of viruses and their possible roles in major evolutionary transitions](https://doi.org/10.1016/j.virusres.2006.01.010). *Virus Research* **117**, 5–16 (2006).

450.

Boeke, J. & Stoye, J. [Retrotransposons, Endogenous Retroviruses, and the Evolution of Retroelement](https://www.ncbi.nlm.nih.gov/books/NBK19468). in *Retroviruses* (eds. Coffin, J. M., Hughes, S. H. & Varmus, H. E.) (Cold Spring Harbor Laboratory Press, 1997).

451.

Kojima, S. *et al.* [Virus-like insertions with sequence signatures similar to those of endogenous nonretroviral RNA viruses in the human genome](https://doi.org/10.1073/pnas.2010758118). *Proceedings of the National Academy of Sciences* **118**, e2010758118 (2021).

452.

Löwer, R., Löwer, J. & R Kurth. [The viruses in all of us: Characteristics and biological significance of human endogenous retrovirus sequences.](https://doi.org/10.1073/pnas.93.11.5177) *Proceedings of the National Academy of Sciences* **93**, 5177–5184 (1996).

453.

Griffiths, D. J. [Endogenous retroviruses in the human genome sequence](https://doi.org/10.1186/gb-2001-2-6-reviews1017). *Genome Biol* **2**, reviews1017.1 (2001).

454.

Baltimore, D. [Expression of animal virus genomes](https://doi.org/10.1128/br.35.3.235-241.1971). *Bacteriol Rev* **35**, 235–241 (1971).

455.

Koonin, E. V., Krupovic, M. & Agol, V. I. [The Baltimore Classification of Viruses 50 Years Later: How Does It Stand in the Light of Virus Evolution?](https://doi.org/10.1128/mmbr.00053-21) *Microbiology and Molecular Biology Reviews* **85**, e00053–21 (2021).

456.

Domingo, E. & Perales, C. RNA Virus Genomes. in *eLS* 1–12 (John Wiley & Sons, Ltd, 2018). doi:[10.1002/9780470015902.a0001488.pub3](https://doi.org/10.1002/9780470015902.a0001488.pub3).

457.

McGeoch, D. J., Rixon, F. J. & Davison, A. J. [Topics in herpesvirus genomics and evolution](https://doi.org/10.1016/j.virusres.2006.01.002). *Virus Research* **117**, 90–104 (2006).

458.

Boehmer, P. & Nimonkar, A. [Herpes Virus Replication](https://doi.org/10.1080/1521654031000070645). *IUBMB Life* **55**, 13–22 (2003).

459.

Brentjens, M. H., Yeung-Yue, K. A., Lee, P. C. & Tyring, S. K. [Human papillomavirus: A review](https://doi.org/10.1016/s0733-8635\(01\)00028-6). *Dermatologic Clinics* **20**, 315–331 (2002).

460.

Kay, A. & Zoulim, F. [Hepatitis B virus genetic variability and evolution](https://doi.org/10.1016/j.virusres.2007.02.021). *Virus Research* **127**, 164–176 (2007).

461.

Parashar, U. D., Bresee, J. S., Gentsch, J. R. & Glass, R. I. [Rotavirus.](https://doi.org/10.3201/eid0404.980406) *Emerg Infect Dis* **4**, 561–570 (1998).

462.

Simmonds, P. [Variability of hepatitis C virus](https://doi.org/10.1016/0270-9139\(95\)90121-3). *Hepatology* **21**, 570–583 (1995).

463.

Wimmer, E., Hellen, C. U. T. & Cao, X. [Genetics of poliovirus](https://doi.org/10.1146/annurev.ge.27.120193.002033). *Annual Review of Genetics* **27**, 353–437 (1993).

464.

Racaniello, V. R. [One hundred years of poliovirus pathogenesis](https://doi.org/10.1016/j.virol.2005.09.015). *Virology* **344**, 9–16 (2006).

465.

Palese, P., Zheng, H., Engelhardt, O. G., Pleschka, S. & García-Sastre, A. [Negative-strand RNA viruses: Genetic engineering and applications.](https://doi.org/10.1073/pnas.93.21.11354) *Proceedings of the National Academy of Sciences* **93**, 11354–11358 (1996).

466.

Domingo, E. & Perales, C. Virus Evolution. in *eLS* (John Wiley & Sons, Ltd, 2014). doi:[10.1002/9780470015902.a0000436.pub3](https://doi.org/10.1002/9780470015902.a0000436.pub3).

467.

V’kovski, P., Kratzel, A., Steiner, S., Stalder, H. & Thiel, V. [Coronavirus biology and replication: Implications for SARS-CoV-2](https://doi.org/10.1038/s41579-020-00468-6). *Nat Rev Microbiol* **19**, 155–170 (2021).

468.

Bäck, A. T. & Lundkvist, Å. [Dengue viruses – an overview](https://doi.org/10.3402/iee.v3i0.19839). *Infect Ecol Epidemiol* **3**, 10.3402/iee.v3i0.19839 (2013).

469.

Dustin, L. B., Bartolini, B., Capobianchi, M. R. & Pistello, M. [Hepatitis C virus: Life cycle in cells, infection and host response, and analysis of molecular markers influencing the outcome of infection and response to therapy](https://doi.org/10.1016/j.cmi.2016.08.025). *Clin Microbiol Infect* **22**, 826–832 (2016).

470.

Kadaja, M., Silla, T., Ustav, E. & Ustav, M. [Papillomavirus DNA replication — From initiation to genomic instability](https://doi.org/10.1016/j.virol.2008.11.032). *Virology* **384**, 360–368 (2009).

471.

Weller, S. K. & Coen, D. M. [Herpes Simplex Viruses: Mechanisms of DNA Replication](https://doi.org/10.1101/cshperspect.a013011). *Cold Spring Harb Perspect Biol* **4**, a013011 (2012).

472.

Beck, J. & Nassal, M. [Hepatitis B virus replication](https://doi.org/10.3748/wjg.v13.i1.48). *World J Gastroenterol* **13**, 48–64 (2007).

473.

Pyle, J. D. & Scholthof, K.-B. G. Chapter 58 - Biology and Pathogenesis of Satellite Viruses. in *Viroids and Satellites* (eds. Hadidi, A., Flores, R., Randles, J. W. & Palukaitis, P.) 627–636 (Academic Press, 2017). doi:[10.1016/b978-0-12-801498-1.00058-9](https://doi.org/10.1016/b978-0-12-801498-1.00058-9).

474.

Raoult, D. *et al.* [The 1.2-megabase genome sequence of Mimivirus](https://doi.org/10.1126/science.1101485). *Science* **306**, 1344–1350 (2004).

475.

Campillo-Balderas, J. A., Lazcano, A. & Becerra, A. [Viral Genome Size Distribution Does not Correlate with the Antiquity of the Host Lineages](https://doi.org/10.3389/fevo.2015.00143). *Frontiers in Ecology and Evolution* **3**, (2015).

476.

Cann, A. J. Virus Structure. in *eLS* 1–9 (John Wiley & Sons, Ltd, 2015). doi:[10.1002/9780470015902.a0000439.pub2](https://doi.org/10.1002/9780470015902.a0000439.pub2).

477.

Hladik, F. & McElrath, M. J. [Setting the stage: Host invasion by HIV](https://doi.org/10.1038/nri2302). *Nat Rev Immunol* **8**, 447–457 (2008).

478.

Shaw, G. M. & Hunter, E. [HIV Transmission](https://doi.org/10.1101/cshperspect.a006965). *Cold Spring Harb Perspect Med* **2**, a006965 (2012).

479.

Weiss, R. A. [How Does HIV Cause AIDS?](https://doi.org/10.1126/science.8493571) *Science* **260**, 1273–1279 (1993).

480.

Melhuish, A. & Lewthwaite, P. [Natural history of HIV and AIDS](https://doi.org/10.1016/j.mpmed.2018.03.010). *Medicine* **46**, 356–361 (2018).

481.

Murray, J. F. *et al.* [Pulmonary complications of the acquired immunodeficiency syndrome](https://doi.org/10.1056/nejm198406213102529). *New England Journal of Medicine* **310**, 1682–1688 (1984).

482.

Sampath, S. *et al.* [Pandemics Throughout the History](https://doi.org/10.7759/cureus.18136). *Cureus* **13**, (2021).

483.

World Health Organization. *[Global report: UNAIDS report on the global AIDS epidemic 2010.](https://www.unaids.org/globalreport/Global_report.htm)* (World Health Organization, 2010).

484.

Barré-Sinoussi, F. *et al.* [Isolation of a T-lymphotropic retrovirus from a patient at risk for acquired immune deficiency syndrome (AIDS)](https://doi.org/10.1126/science.6189183). *Science* **220**, 868–871 (1983).

485.

Gallo, R. C. *et al.* [Isolation of human T-cell leukemia virus in acquired immune deficiency syndrome (AIDS)](https://doi.org/10.1126/science.6601823). *Science* **220**, 865–867 (1983).

486.

Clavel, F. *et al.* [Isolation of a New Human Retrovirus from West African Patients with AIDS](https://doi.org/10.1126/science.2425430). *Science* **233**, 343–346 (1986).

487.

Gilbert, P. B. *et al.* [Comparison of HIV-1 and HIV-2 infectivity from a prospective cohort study in Senegal](https://doi.org/10.1002/sim.1342). *Statistics in Medicine* **22**, 573–593 (2003).

488.

van der Loeff, M. F. S. *et al.* [Sixteen years of HIV surveillance in a West African research clinic reveals divergent epidemic trends of HIV-1 and HIV-2](https://doi.org/10.1093/ije/dyl037). *Int J Epidemiol* **35**, 1322–1328 (2006).

489.

Gao, F. *et al.* [Origin of HIV-1 in the chimpanzee Pan troglodytes troglodytes](https://doi.org/10.1038/17130). *Nature* **397**, 436–441 (1999).

491.

Sharp, P. M. & Hahn, B. H. [Origins of HIV and the AIDS Pandemic](https://doi.org/10.1101/cshperspect.a006841). *Cold Spring Harb Perspect Med* **1**, a006841 (2011).

492.

Hirsch, V. M., Olmsted, R. A., Murphey-Corb, M., Purcell, R. H. & Johnson, P. R. [An African primate lentivirus (SIVsmclosely related to HIV-2](https://doi.org/10.1038/339389a0). *Nature* **339**, 389–392 (1989).

494.

Chen, Z. *et al.* [Genetic characterization of new West African simian immunodeficiency virus SIVsm: Geographic clustering of household-derived SIV strains with human immunodeficiency virus type 2 subtypes and genetically diverse viruses from a single feral sooty mangabey troop](https://doi.org/10.1128/jvi.70.6.3617-3627.1996). *J Virol* **70**, 3617–3627 (1996).

495.

Hemelaar, J. [The origin and diversity of the HIV-1 pandemic](https://doi.org/10.1016/j.molmed.2011.12.001). *Trends in Molecular Medicine* **18**, 182–192 (2012).

496.

Worobey, M. *et al.* [Direct evidence of extensive diversity of HIV-1 in Kinshasa by 1960](https://doi.org/10.1038/nature07390). *Nature* **455**, 661–664 (2008).

498.

Faria, N. R. *et al.* [The early spread and epidemic ignition of HIV-1 in human populations](https://doi.org/10.1126/science.1256739). *Science* **346**, 56–61 (2014).

499.

Korber, B. *et al.* [Timing the ancestor of the HIV-1 pandemic strains](https://doi.org/10.1126/science.288.5472.1789). *Science* **288**, 1789–1796 (2000).

500.

Rambaut, A., Posada, D., Crandall, K. A. & Holmes, E. C. [The causes and consequences of HIV evolution](https://doi.org/10.1038/nrg1246). *Nat Rev Genet* **5**, 52–61 (2004).

501.

McCutchan, F. E. [Global epidemiology of HIV](https://doi.org/10.1002/jmv.20599). *Journal of Medical Virology* **78**, S7–s12 (2006).

502.

Pérez-Losada, M., Arenas, M., Galán, J. C., Palero, F. & González-Candelas, F. [Recombination in viruses: Mechanisms, methods of study, and evolutionary consequences](https://doi.org/10.1016/j.meegid.2014.12.022). *Infect Genet Evol* **30**, 296–307 (2015).

503.

Robertson, D. L., Hahn, B. H. & Sharp, P. M. [Recombination in AIDS viruses](https://doi.org/10.1007/bf00163230). *J Mol Evol* **40**, 249–259 (1995).

504.

HIV Circulating Recombinant Forms (CRFs). [https://www.hiv.lanl.gov/content/sequence/HIV/CRFs/CRFs.html](https://www.hiv.lanl.gov/content/sequence/HIV/CRFs/CRFs.html).

505.

Lau, K. A. & Wong, J. J. L. [Current Trends of HIV Recombination Worldwide](https://doi.org/10.4081/idr.2013.s1.e4). *Infect Dis Rep* **5**, e4 (2013).

506.

Posada, D., Crandall, K. A. & Holmes, E. C. [Recombination in evolutionary genomics](https://doi.org/10.1146/annurev.genet.36.040202.111115). *Annu Rev Genet* **36**, 75–97 (2002).

507.

Taylor, B. S., Sobieszczyk, M. E., McCutchan, F. E. & Hammer, S. M. [The Challenge of HIV-1 Subtype Diversity](https://doi.org/10.1056/NEJMra0706737). *New England Journal of Medicine* **358**, 1590–1602 (2008).

508.

Hemelaar, J., Gouws, E., Ghys, P. D. & Osmanov, S. [Global trends in molecular epidemiology of HIV-1 during 2000–2007](https://doi.org/10.1097/QAD.0b013e328342ff93). *Aids* **25**, 679–689 (2011).

509.

Distribution of all HIV-1 sequences: WORLD. [https://www.hiv.lanl.gov/components/sequence/HIV/geo/geo.comp](https://www.hiv.lanl.gov/components/sequence/HIV/geo/geo.comp).

510.

Freed, E. O. [HIV-1 Replication](https://doi.org/10.1023/a:1021070512287). *Somat Cell Mol Genet* **26**, 13–33 (2001).

511.

Ferguson, M. R., Rojo, D. R., von Lindern, J. J. & O’Brien, W. A. [HIV-1 replication cycle](https://doi.org/10.1016/s0272-2712\(02\)00015-x). *Clin Lab Med* **22**, 611–635 (2002).

512.

Gougeon, M. L., Laurent-Crawford, A. G., Hovanessian, A. G. & Montagnier, L. [Direct and indirect mechanisms mediating apoptosis during HIV infection: Contribution to in vivo CD4 T cell depletion](https://doi.org/10.1006/smim.1993.1022). *Seminars in Immunology* **5**, 187–194 (1993).

513.

Vidya Vijayan, K. K., Karthigeyan, K. P., Tripathi, S. P. & Hanna, L. E. [Pathophysiology of CD4+ T-Cell Depletion in HIV-1 and HIV-2 Infections](https://doi.org/10.3389/fimmu.2017.00580). *Front Immunol* **8**, 580 (2017).

514.

Frankel, A. D. & Young, J. A. [HIV-1: Fifteen proteins and an RNA](https://doi.org/10.1146/annurev.biochem.67.1.1). *Annu Rev Biochem* **67**, 1–25 (1998).

515.

Fossen, T. *et al.* [Solution Structure of the Human Immunodeficiency Virus Type 1 P6 Protein \*](https://doi.org/10.1074/jbc.M507375200). *Journal of Biological Chemistry* **280**, 42515–42527 (2005).

516.

Göttlinger, H. G., Dorfman, T., Sodroski, J. G. & Haseltine, W. A. [Effect of mutations affecting the P6 gag protein on human immunodeficiency virus particle release.](https://doi.org/10.1073/pnas.88.8.3195) *Proceedings of the National Academy of Sciences* **88**, 3195–3199 (1991).

517.

Huang, M., Orenstein, J. M., Martin, M. A. & Freed, E. O. [p6Gag is required for particle production from full-length human immunodeficiency virus type 1 molecular clones expressing protease](https://doi.org/10.1128/jvi.69.11.6810-6818.1995). *Journal of Virology* **69**, 6810–6818 (1995).

518.

Bour, S., Geleziunas, R. & Wainberg, M. A. [The human immunodeficiency virus type 1 (HIV-1) CD4 receptor and its central role in promotion of HIV-1 infection](https://doi.org/10.1128/mr.59.1.63-93.1995). *Microbiological Reviews* **59**, 63–93 (1995).

519.

Hernandez, L. D., Hoffman, L. R., Wolfsberg, T. G. & White, J. M. [Virus-cell and cell-cell fusion](https://doi.org/10.1146/annurev.cellbio.12.1.627). *Annu Rev Cell Dev Biol* **12**, 627–661 (1996).

520.

Jones, K. & Peterlin, B. [Control of Rna Initiation and Elongation at the Hiv-1 Promoter](https://doi.org/10.1146/annurev.bi.63.070194.003441). *Annu. Rev. Biochem.* **63**, 717–743 (1994).

521.

Hope, T. J. [Viral RNA export](https://doi.org/10.1016/s1074-5521\(97\)90124-1). *Chemistry & Biology* **4**, 335–344 (1997).

522.

Mangasarian, A. & Trono, D. [The multifaceted role of HIV Nef](https://doi.org/10.1016/s0923-2516\(97\)81909-7). *Research in Virology* **148**, 30–33 (1997).

523.

Cohen, é. A., Subbramanian, R. A. & Göttlinger, H. G. Role of Auxiliary Proteins in Retroviral Morphogenesis. in *Morphogenesis and Maturation of Retroviruses* (ed. Kräusslich, H.-G.) 219–235 (Springer, 1996). doi:[10.1007/978-3-642-80145-7\_7](https://doi.org/10.1007/978-3-642-80145-7_7).

524.

Lamb, R. A. & Pinto, L. H. [Do Vpu and Vpr of Human Immunodeficiency Virus Type 1 and NB of Influenza B Virus Have Ion Channel Activities in the Viral Life Cycles?](https://doi.org/10.1006/viro.1997.8451) *Virology* **229**, 1–11 (1997).

525.

Khan, N. & Geiger, J. D. [Role of Viral Protein U (Vpu) in HIV-1 Infection and Pathogenesis](https://doi.org/10.3390/v13081466). *Viruses* **13**, 1466 (2021).

526.

Emerman, M. [HIV-1, Vpr and the cell cycle](https://doi.org/10.1016/s0960-9822\(02\)00676-0). *Current Biology* **6**, 1096–1103 (1996).

527.

Miller, R. H. [Human immunodeficiency virus may encode a novel protein on the genomic DNA plus strand](https://doi.org/10.1126/science.3347840). *Science* **239**, 1420–1422 (1988).

528.

Briquet, S. & Vaquero, C. [Immunolocalization Studies of an Antisense Protein in HIV-1-Infected Cells and Viral Particles](https://doi.org/10.1006/viro.2001.1224). *Virology* **292**, 177–184 (2002).

529.

Cassan, E., Arigon-Chifolleau, A.-M., Mesnard, J.-M., Gross, A. & Gascuel, O. [Concomitant emergence of the antisense protein gene of HIV-1 and of the pandemic](https://doi.org/10.1073/pnas.1605739113). *Pnas* **113**, 11537–11542 (2016).

530.

Savoret, J. *et al.* [A Pilot Study of the Humoral Response Against the AntiSense Protein (ASP) in HIV-1-Infected Patients](https://doi.org/10.3389/fmicb.2020.00020). *Frontiers in Microbiology* **11**, (2020).

531.

Zardecki, C. *et al.* [PDB-101: Educational resources supporting molecular explorations through biology and medicine](https://doi.org/10.1002/pro.4200). *Protein Science* **31**, 129–140 (2022).

532.

Eisinger, R. W., Dieffenbach, C. W. & Fauci, A. S. [HIV Viral Load and Transmissibility of HIV Infection: Undetectable Equals Untransmittable](https://doi.org/10.1001/jama.2018.21167). *Jama* **321**, 451–452 (2019).

533.

Palella, F. J. *et al.* [Declining Morbidity and Mortality among Patients with Advanced Human Immunodeficiency Virus Infection](https://doi.org/10.1056/nejm199803263381301). *New England Journal of Medicine* **338**, 853–860 (1998).

534.

Forsythe, S. S. *et al.* [Twenty Years Of Antiretroviral Therapy For People Living With HIV: Global Costs, Health Achievements, Economic Benefits](https://doi.org/10.1377/hlthaff.2018.05391). *Health Affairs* **38**, 1163–1172 (2019).

535.

Fischl, M. A. *et al.* [The Efficacy of Azidothymidine (AZT) in the Treatment of Patients with AIDS and AIDS-Related Complex](https://doi.org/10.1056/nejm198707233170401). *New England Journal of Medicine* **317**, 185–191 (1987).

536.

Richman, D. D. [Susceptibility to nucleoside analogues of zidovudine-resistant isolates of human immunodeficiency virus](https://doi.org/10.1016/0002-9343\(90\)90414-9). *The American Journal of Medicine* **88**, S8–s10 (1990).

537.

Yeo, J. Y., Goh, G.-R., Su, C. T.-T. & Gan, S. K.-E. [The Determination of HIV-1 RT Mutation Rate, Its Possible Allosteric Effects, and Its Implications on Drug Resistance](https://doi.org/10.3390/v12030297). *Viruses* **12**, 297 (2020).

538.

Cuevas, J. M., Geller, R., Garijo, R., López-Aldeguer, J. & Sanjuán, R. [Extremely High Mutation Rate of HIV-1 In Vivo](https://doi.org/10.1371/journal.pbio.1002251). *PLOS Biology* **13**, e1002251 (2015).

539.

Carvajal-Rodríguez, A., Crandall, K. A. & Posada, D. [Recombination favors the evolution of drug resistance in HIV-1 during antiretroviral therapy](https://doi.org/10.1016/j.meegid.2007.02.001). *Infect Genet Evol* **7**, 476–483 (2007).

540.

Gulick, R. M. *et al.* [Treatment with indinavir, zidovudine, and lamivudine in adults with human immunodeficiency virus infection and prior antiretroviral therapy](https://doi.org/10.1056/nejm199709113371102). *N Engl J Med* **337**, 734–739 (1997).

541.

Wensing, A. M. J., van Maarseveen, N. M. & Nijhuis, M. [Fifteen years of HIV Protease Inhibitors: Raising the barrier to resistance](https://doi.org/10.1016/j.antiviral.2009.10.003). *Antiviral Research* **85**, 59–74 (2010).

542.

Pedersen, O. S. & Pedersen, E. B. [Non-Nucleoside Reverse Transcriptase Inhibitors: The NNRTI Boom](https://doi.org/10.1177/095632029901000601). *Antivir Chem Chemother* **10**, 285–314 (1999).

543.

Scarsi, K. K., Havens, J. P., Podany, A. T., Avedissian, S. N. & Fletcher, C. V. [HIV-1 Integrase Inhibitors: A Comparative Review of Efficacy and Safety](https://doi.org/10.1007/s40265-020-01379-9). *Drugs* **80**, 1649–1676 (2020).

544.

Fletcher, C. V. [Enfuvirtide, a new drug for HIV infection](https://doi.org/10.1016/s0140-6736\(03\)13323-5). *The Lancet* **361**, 1577–1578 (2003).

545.

Esté, J. A. & Telenti, A. [HIV entry inhibitors](https://doi.org/10.1016/s0140-6736\(07\)61052-6). *The Lancet* **370**, 81–88 (2007).

546.

Kilby, J. M. & Eron, J. J. [Novel Therapies Based on Mechanisms of HIV-1 Cell Entry](https://doi.org/10.1056/NEJMra022812). *N Engl J Med* **348**, 2228–2238 (2003).

547.

Yeni, P. [Update on HAART in HIV](https://doi.org/10.1016/j.jhep.2005.11.021). *Journal of Hepatology* **44**, S100–s103 (2006).

548.

Palmisano, L. & Vella, S. [A brief history of antiretroviral therapy of HIV infection: Success and challenges](https://doi.org/10.4415/ann_11_01_10). *Ann Ist Super Sanita* **47**, 44–48 (2011).

549.

Pennings, P. S. [HIV drug resistance: Problems and perspectives](https://doi.org/10.4081/idr.2013.s1.e5). *Infectious Disease Reports* **5**, e5 (2013).

550.

Mehta, S., Moore, R. D. & Graham, N. M. H. [Potential factors affecting adherence with HIV therapy](https://doi.org/10.1097/00002030-199714000-00002). *Aids* **11**, 1665–1670 (1997).

551.

Miller, N. H. [Compliance with treatment regimens in chronic asymptomatic diseases](https://doi.org/10.1016/s0002-9343\(97\)00467-1). *The American Journal of Medicine* **102**, 43–49 (1997).

552.

Chesney, M. A., Morin, M. & Sherr, L. [Adherence to HIV combination therapy](https://doi.org/10.1016/s0277-9536\(99\)00468-2). *Social Science & Medicine* **50**, 1599–1605 (2000).

553.

Aldir, I., Horta, A. & Serrado, M. [Single-tablet regimens in HIV: Does it really make a difference?](https://doi.org/10.1185/03007995.2013.844685) *Current Medical Research and Opinion* **30**, 89–97 (2014).

554.

Grant, R. M. *et al.* [Preexposure Chemoprophylaxis for HIV Prevention in Men Who Have Sex with Men](https://doi.org/10.1056/NEJMoa1011205). *N Engl J Med* **363**, 2587–2599 (2010).

556.

Buchbinder, S. P. & Liu, A. [Pre-exposure prophylaxis and the promise of combination prevention approaches](https://doi.org/10.1007/s10461-011-9894-1). *AIDS Behav* **15 Suppl 1**, S72–79 (2011).

557.

Riddell, J., IV, Amico, K. R. & Mayer, K. H. [HIV Preexposure Prophylaxis: A Review](https://doi.org/10.1001/jama.2018.1917). *Jama* **319**, 1261–1268 (2018).

558.

Truvada. [https://www.ema.europa.eu/en/medicines/human/EPAR/truvada](https://www.ema.europa.eu/en/medicines/human/EPAR/truvada) (2018).

559.

About PrEP | PrEP | HIV Basics | HIV/AIDS. [https://www.cdc.gov/hiv/basics/prep/about-prep.html](https://www.cdc.gov/hiv/basics/prep/about-prep.html) (2022).

560.

Zolopa, A. R. [The evolution of HIV treatment guidelines: Current state-of-the-art of ART](https://doi.org/10.1016/j.antiviral.2009.10.018). *Antiviral Research* **85**, 241–244 (2010).

561.

Organization, W. H. *Consolidated guidelines on HIV prevention, testing, treatment, service delivery and monitoring: Recommendations for a public health approach*. [https://www.who.int/publications-detail-redirect/9789240031593](https://www.who.int/publications-detail-redirect/9789240031593) (2021).

562.

Ammaranond, P. & Sanguansittianan, S. [Mechanism of HIV antiretroviral drugs progress toward drug resistance](https://doi.org/10.1111/j.1472-8206.2011.01009.x). *Fundamental & Clinical Pharmacology* **26**, 146–161 (2012).

563.

Clavel, F. & Hance, A. J. [HIV Drug Resistance](https://doi.org/10.1056/NEJMra025195). *New England Journal of Medicine* **350**, 1023–1035 (2004).

564.

Sarafianos, S. G. *et al.* [Structure and function of HIV-1 reverse transcriptase: Molecular mechanisms of polymerization and inhibition](https://doi.org/10.1016/j.jmb.2008.10.071). *J Mol Biol* **385**, 693–713 (2009).

565.

Goodsell, D. S., Autin, L. & Olson, A. J. [Illustrate: Software for Biomolecular Illustration](https://doi.org/10.1016/j.str.2019.08.011). *Structure* **27**, 1716–1720.e1 (2019).

566.

Esnouf, R. M. *et al.* [Unique features in the structure of the complex between HIV-1 reverse transcriptase and the bis(heteroaryl)piperazine (BHAP) U-90152 explain resistance mutations for this nonnucleoside inhibitor](https://doi.org/10.1073/pnas.94.8.3984). *Proc Natl Acad Sci U S A* **94**, 3984–3989 (1997).

567.

Hang, J. Q. *et al.* [Activity of the isolated HIV RNase H domain and specific inhibition by N-hydroxyimides](https://doi.org/10.1016/j.bbrc.2004.03.061). *Biochemical and Biophysical Research Communications* **317**, 321–329 (2004).

568.

Klumpp, K. & Mirzadegan, T. [Recent Progress in the Design of Small Molecule Inhibitors of HIV RNase H](https://doi.org/10.2174/138161206776873653). *Current Pharmaceutical Design* **12**, 1909–1922 (2006).

569.

Menéndez-Arias, L. [Mechanisms of resistance to nucleoside analogue inhibitors of HIV-1 reverse transcriptase](https://doi.org/10.1016/j.virusres.2007.12.015). *Virus Research* **134**, 124–146 (2008).

570.

Sluis-Cremer, N., Arion, D. & Parniak\*, M. A. [Molecular mechanisms of HIV-1 resistance to nucleoside reverse transcriptase inhibitors (NRTIs)](https://doi.org/10.1007/pl00000626). *CMLS, Cell. Mol. Life Sci.* **57**, 1408–1422 (2000).

571.

Sarafianos, S. G. *et al.* [Lamivudine (3TC) resistance in HIV-1 reverse transcriptase involves steric hindrance with beta-branched amino acids](https://doi.org/10.1073/pnas.96.18.10027). *Proc Natl Acad Sci U S A* **96**, 10027–10032 (1999).

572.

Meyer, P. R., Matsuura, S. E., Mian, A. M., So, A. G. & Scott, W. A. [A mechanism of AZT resistance: An increase in nucleotide-dependent primer unblocking by mutant HIV-1 reverse transcriptase](https://doi.org/10.1016/s1097-2765\(00\)80185-9). *Mol Cell* **4**, 35–43 (1999).

573.

Boyer, P. L., Sarafianos, S. G., Arnold, E. & Hughes, S. H. [Selective Excision of AZTMP by Drug-Resistant Human Immunodeficiency Virus Reverse Transcriptase](https://doi.org/10.1128/jvi.75.10.4832-4842.2001). *J Virol* **75**, 4832–4842 (2001).

574.

Deeks, S. G. [Nonnucleoside Reverse Transcriptase Inhibitor Resistance](https://doi.org/10.1097/00126334-200103011-00004). *JAIDS Journal of Acquired Immune Deficiency Syndromes* **26**, S25 (2001).

575.

Ren, J. & Stammers, D. K. [Structural basis for drug resistance mechanisms for non-nucleoside inhibitors of HIV reverse transcriptase](https://doi.org/10.1016/j.virusres.2007.12.018). *Virus Research* **134**, 157–170 (2008).

576.

Lloyd, S. B., Kent, S. J. & Winnall, W. R. [The High Cost of Fidelity](https://doi.org/10.1089/aid.2013.0153). *AIDS Research and Human Retroviruses* **30**, 8–16 (2014).

577.

Pearl, L. H. & Taylor, W. R. [A structural model for the retroviral proteases](https://doi.org/10.1038/329351a0). *Nature* **329**, 351–354 (1987).

578.

Gulnik, S., Erickson, J. W. & Xie, D. [HIV protease: Enzyme function and drug resistance](https://doi.org/10.1016/s0083-6729\(00\)58026-1). in *Vitamins & Hormones* vol. 58 213–256 (Academic Press, 2000).

579.

Silva, A. M., Cachau, R. E., Sham, H. L. & Erickson, J. W. [Inhibition and catalytic mechanism of HIV-1 aspartic protease](https://doi.org/10.1006/jmbi.1996.0026). *Journal of Molecular Biology* **255**, 321–340 (1996).

580.

Hornak, V., Okur, A., Rizzo, R. C. & Simmerling, C. [HIV-1 protease flaps spontaneously open and reclose in molecular dynamics simulations](https://doi.org/10.1073/pnas.0508452103). *Proceedings of the National Academy of Sciences* **103**, 915–920 (2006).

581.

Freedberg, D. I. *et al.* [Rapid structural fluctuations of the free HIV protease flaps in solution: Relationship to crystal structures and comparison with predictions of dynamics calculations](https://doi.org/10.1110/ps.33202). *Protein Sci* **11**, 221–232 (2002).

582.

Yu, Y. *et al.* [Structural insights into HIV-1 protease flap opening processes and key intermediates](https://doi.org/10.1039/c7ra09691g). *RSC Adv.* **7**, 45121–45128 (2017).

583.

Roberts, N. A. *et al.* [Rational Design of Peptide-Based HIV Proteinase Inhibitors](https://doi.org/10.1126/science.2183354). *Science* **248**, 358–361 (1990).

584.

Lv, Z., Chu, Y. & Wang, Y. [HIV protease inhibitors: A review of molecular selectivity and toxicity](https://doi.org/10.2147/hiv.s79956). *HIV AIDS (Auckl)* **7**, 95–104 (2015).

585.

Prabu-Jeyabalan, M., Nalivaika, E. & Schiffer, C. A. [Substrate Shape Determines Specificity of Recognition for HIV-1 Protease: Analysis of Crystal Structures of Six Substrate Complexes](https://doi.org/10.1016/s0969-2126\(02\)00720-7). *Structure* **10**, 369–381 (2002).

586.

Prabu-Jeyabalan, M. *et al.* [Substrate Envelope and Drug Resistance: Crystal Structure of RO1 in Complex with Wild-Type Human Immunodeficiency Virus Type 1 Protease](https://doi.org/10.1128/aac.50.4.1518-1521.2006). *Antimicrob Agents Chemother* **50**, 1518–1521 (2006).

587.

Kurt Yilmaz, N., Swanstrom, R. & Schiffer, C. A. [Improving Viral Protease Inhibitors to Counter Drug Resistance](https://doi.org/10.1016/j.tim.2016.03.010). *Trends in Microbiology* **24**, 547–557 (2016).

588.

Chiu, T. K. & Davies, D. R. [Structure and Function of HIV-1 Integrase](https://doi.org/10.2174/1568026043388547). *Current Topics in Medicinal Chemistry* **4**, 965–977 (2004).

589.

Esposito, D. & Craigie, R. [HIV Integrase Structure and Function](https://doi.org/10.1016/s0065-3527\(08\)60304-8). in *Advances in Virus Research* (eds. Rlaramorosch, K., Murphy, F. A. & Shawn, A. J.) vol. 52 319–333 (Academic Press, 1999).

590.

Delelis, O., Carayon, K., Saïb, A., Deprez, E. & Mouscadet, J.-F. [Integrase and integration: Biochemical activities of HIV-1 integrase](https://doi.org/10.1186/1742-4690-5-114). *Retrovirology* **5**, 114 (2008).

591.

Maertens, G. N., Engelman, A. N. & Cherepanov, P. [Structure and function of retroviral integrase](https://doi.org/10.1038/s41579-021-00586-9). *Nat Rev Microbiol* **20**, 20–34 (2022).

592.

Pommier, Y., Johnson, A. A. & Marchand, C. [Integrase inhibitors to treat HIV/Aids](https://doi.org/10.1038/nrd1660). *Nat Rev Drug Discov* **4**, 236–248 (2005).

593.

Blanco, J.-L., Varghese, V., Rhee, S.-Y., Gatell, J. M. & Shafer, R. W. [HIV-1 Integrase Inhibitor Resistance and Its Clinical Implications](https://doi.org/10.1093/infdis/jir025). *The Journal of Infectious Diseases* **203**, 1204–1214 (2011).

594.

Geretti, A. M., Armenia, D. & Ceccherini-Silberstein, F. [Emerging patterns and implications of HIV-1 integrase inhibitor resistance](https://doi.org/10.1097/QCO.0b013e32835a1de7). *Current Opinion in Infectious Diseases* **25**, 677–686 (2012).

595.

Knox, D. C., Anderson, P. L., Harrigan, P. R. & Tan, D. H. S. [Multidrug-Resistant HIV-1 Infection despite Preexposure Prophylaxis](https://doi.org/10.1056/NEJMc1611639). *N Engl J Med* **376**, 501–502 (2017).

596.

Hurt, C. B., Eron, J. J. & Cohen, M. S. [Pre-exposure prophylaxis and antiretroviral resistance: HIV prevention at a cost?](https://doi.org/10.1093/cid/cir684) *Clin Infect Dis* **53**, 1265–1270 (2011).

597.

Gibas, K. M., van den Berg, P., Powell, V. E. & Krakower, D. S. [Drug Resistance During HIV Pre-Exposure Prophylaxis](https://doi.org/10.1007/s40265-019-01108-x). *Drugs* **79**, 609–619 (2019).

598.

Mourad, R. *et al.* [A phylotype-based analysis highlights the role of drug-naive HIV-positive individuals in the transmission of antiretroviral resistance in the UK](https://doi.org/10.1097/qad.0000000000000768). *Aids* **29**, 1917–1925 (2015).

599.

Hué, S. *et al.* [Demonstration of Sustained Drug-Resistant Human Immunodeficiency Virus Type 1 Lineages Circulating among Treatment-Naïve Individuals](https://doi.org/10.1128/jvi.01556-08). *Journal of Virology* **83**, 2645–2654 (2009).

600.

Drescher, S. M. *et al.* [Treatment-Naive Individuals Are the Major Source of Transmitted HIV-1 Drug Resistance in Men Who Have Sex With Men in the Swiss HIV Cohort Study](https://doi.org/10.1093/cid/cit694). *Clinical Infectious Diseases* **58**, 285–294 (2014).

601.

Boerma, R. S. *et al.* [High levels of pre-treatment HIV drug resistance and treatment failure in Nigerian children](https://doi.org/10.7448/ias.19.1.21140). *Journal of the International AIDS Society* **19**, 21140 (2016).

602.

Clutter, D. S., Jordan, M. R., Bertagnolio, S. & Shafer, R. W. [HIV-1 drug resistance and resistance testing](https://doi.org/10.1016/j.meegid.2016.08.031). *Infection, Genetics and Evolution* **46**, 292–307 (2016).

603.

Kühnert, D. *et al.* [Quantifying the fitness cost of HIV-1 drug resistance mutations through phylodynamics](https://doi.org/10.1371/journal.ppat.1006895). *PLOS Pathogens* **14**, e1006895 (2018).

604.

Mesplède, T. *et al.* [Viral fitness cost prevents HIV-1 from evading dolutegravir drug pressure](https://doi.org/10.1186/1742-4690-10-22). *Retrovirology* **10**, 22 (2013).

605.

Castro, H. *et al.* [Persistence of HIV-1 Transmitted Drug Resistance Mutations](https://doi.org/10.1093/infdis/jit345). *J Infect Dis* **208**, 1459–1463 (2013).

606.

Blassel, L. *et al.* [Drug resistance mutations in HIV: New bioinformatics approaches and challenges](https://doi.org/10.1016/j.coviro.2021.09.009). *Current Opinion in Virology* **51**, 56–64 (2021).

607.

Committee, U. C. S. [The creation of a large UK-based multicentre cohort of HIV-infected individuals: The UK Collaborative HIV Cohort (UK CHIC) Study](https://doi.org/10.1111/j.1468-1293.2004.00197.x). *HIV Medicine* **5**, 115–124 (2004).

608.

Abeler-Dörner, L. *et al.* [PANGEA-HIV 2: Phylogenetics And Networks for Generalised Epidemics in Africa](https://doi.org/10.1097/coh.0000000000000542). *Current Opinion in HIV and AIDS* **14**, 173–180 (2019).

609.

Shafer, R. W. [Rationale and Uses of a Public HIV Drug‐Resistance Database](https://doi.org/10.1086/505356). *J Infect Dis* **194**, S51–s58 (2006).

610.

Kuiken, C., Korber, B. & Shafer, R. W. [HIV Sequence Databases](https://www.ncbi.nlm.nih.gov/pmc/articles/Pmc2613779). *AIDS Rev* **5**, 52–61 (2003).

611.

Wensing, A. M. *et al.* [2019 update of the drug resistance mutations in HIV-1](https://www.ncbi.nlm.nih.gov/pmc/articles/Pmc6892618). *Top Antivir Med* **27**, 111–121 (2019).

612.

Clark, S. A., Calef, C. & Mellors, J. W. [Mutations in retroviral genes associated with drug resistance](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.625.1084&rep=rep1&type=pdf). *HIV sequence compendium* 58–158 (2007).

613.

Liu, T. F. & Shafer, R. W. [Web Resources for HIV Type 1 Genotypic-Resistance Test Interpretation](https://doi.org/10.1086/503914). *Clin Infect Dis* **42**, 1608–1618 (2006).

614.

Johnson, V. A. *et al.* [Update of the Drug Resistance Mutations in HIV-1: March 2013](https://www.ncbi.nlm.nih.gov/pmc/articles/Pmc6148891). *Top Antivir Med* **21**, 6–7 (2016).

615.

Villabona-Arenas, C. J. *et al.* [In-depth analysis of HIV-1 drug resistance mutations in HIV-infected individuals failing first-line regimens in West and Central Africa](https://doi.org/10.1097/qad.0000000000001233). *Aids* **30**, 2577 (2016).

616.

Shulman, N. S., Bosch, R. J., Mellors, J. W., Albrecht, M. A. & Katzenstein, D. A. [Genetic correlates of efavirenz hypersusceptibility](https://doi.org/10.1097/00002030-200409030-00006). *Aids* **18**, 1781–1785 (2004).

617.

Miller, M. D. *et al.* [Genotypic and Phenotypic Predictors of the Magnitude of Response to Tenofovir Disoproxil Fumarate Treatment in Antiretroviral-Experienced Patients](https://doi.org/10.1086/381784). *The Journal of Infectious Diseases* **189**, 837–846 (2004).

618.

Brown, B. W. & Russell, K. [Methods correcting for multiple testing: Operating characteristics](https://doi.org/10.1002/\(sici\)1097-0258\(19971130\)16:22%3C2511::aid-sim693%3E3.0.co;2-4). *Statistics in Medicine* **16**, 2511–2528 (1997).

619.

Austin, P. C., Mamdani, M. M., Juurlink, D. N. & Hux, J. E. [Testing multiple statistical hypotheses resulted in spurious associations: A study of astrological signs and health](https://doi.org/10.1016/j.jclinepi.2006.01.012). *Journal of Clinical Epidemiology* **59**, 964–969 (2006).

620.

Hochberg, Y. & Tamhane, A. C. *Multiple comparison procedures*. (1987). doi:[10.1002/9780470316672](https://doi.org/10.1002/9780470316672).

621.

Benjamini, Y. & Hochberg, Y. [Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x). *Journal of the Royal Statistical Society* **57**, 289–300 (1995).

622.

Gonzales, M. J. *et al.* [Extended spectrum of HIV-1 reverse transcriptase mutations in patients receiving multiple nucleoside analog inhibitors](https://doi.org/10.1097/01.aids.0000050860.71999.23). *Aids* **17**, 791–799 (2003).

623.

Seoighe, C. *et al.* [A Model of Directional Selection Applied to the Evolution of Drug Resistance in HIV-1](https://doi.org/10.1093/molbev/msm021). *Molecular Biology and Evolution* **24**, 1025–1031 (2007).

624.

Sham, P. C. & Purcell, S. M. [Statistical power and significance testing in large-scale genetic studies](https://doi.org/10.1038/nrg3706). *Nature Reviews Genetics* **15**, 335–346 (2014).

625.

Alizon, S. *et al.* [Phylogenetic Approach Reveals That Virus Genotype Largely Determines HIV Set-Point Viral Load](https://doi.org/10.1371/journal.ppat.1001123). *PLOS Pathogens* **6**, e1001123 (2010).

626.

Flynn, W. F. *et al.* [Deep Sequencing of Protease Inhibitor Resistant HIV Patient Isolates Reveals Patterns of Correlated Mutations in Gag and Protease](https://doi.org/10.1371/journal.pcbi.1004249). *PLOS Computational Biology* **11**, e1004249 (2015).

627.

Petropoulos, C. J. *et al.* [A Novel Phenotypic Drug Susceptibility Assay for Human Immunodeficiency Virus Type 1](https://doi.org/10.1128/aac.44.4.920-928.2000). *Antimicrobial Agents and Chemotherapy* **44**, 920–928 (2000).

628.

Hertogs, K. *et al.* [A Rapid Method for Simultaneous Detection of Phenotypic Resistance to Inhibitors of Protease and Reverse Transcriptase in Recombinant Human Immunodeficiency Virus Type 1 Isolates from Patients Treated with Antiretroviral Drugs](https://doi.org/10.1128/aac.42.2.269). *Antimicrobial Agents and Chemotherapy* **42**, 269–276 (1998).

629.

Heilek-Snyder, G. & Bean, P. [Role of HIV phenotypic assays in the management of HIV infection](https://europepmc.org/article/med/11975451). *Am Clin Lab* **21**, 40–43 (2002 Jan-Feb).

631.

Gartland, M. *et al.* [Susceptibility of global HIV-1 clinical isolates to fostemsavir using the PhenoSense® Entry assay](https://doi.org/10.1093/jac/dkaa474). *Journal of Antimicrobial Chemotherapy* **76**, 648–652 (2021).

632.

Masquelier, B. *et al.* [Genotypic and Phenotypic Resistance Patterns of Human Immunodeficiency Virus Type 1 Variants with Insertions or Deletions in the Reverse Transcriptase (RT): Multicenter Study of Patients Treated with RT Inhibitors](https://doi.org/10.1128/aac.45.6.1836-1842.2001). *Antimicrobial Agents and Chemotherapy* **45**, 1836–1842 (2001).

633.

Larder, B. A. & Kemp, S. D. [Multiple mutations in HIV-1 reverse transcriptase confer high-level resistance to zidovudine (AZT)](https://doi.org/10.1126/science.2479983). *Science* **246**, 1155–1158 (1989).

634.

de Vreese, K. *et al.* [Resistance of human immunodeficiency virus type 1 reverse transcriptase to TIBO derivatives induced by site-directed mutagenesis](https://doi.org/10.1016/0042-6822\(92\)90550-9). *Virology* **188**, 900–904 (1992).

635.

Tambuyzer, L., Nijs, S., Daems, B., Picchio, G. & Vingerhoets, J. [Effect of Mutations at Position E138 in HIV-1 Reverse Transcriptase on Phenotypic Susceptibility and Virologic Response to Etravirine](https://doi.org/10.1097/QAI.0b013e3182237f74). *JAIDS Journal of Acquired Immune Deficiency Syndromes* **58**, 18–22 (2011).

636.

Katzenstein, D. A. *et al.* [Phenotypic susceptibility and virological outcome in nucleoside-experienced patients receiving three or four antiretroviral drugs](https://doi.org/10.1097/00002030-200304110-00007). *Aids* **17**, 821–830 (2003).

637.

Blassel, L. *et al.* [Using machine learning and big data to explore the drug resistance landscape in HIV](https://doi.org/10.1371/journal.pcbi.1008873). *PLOS Computational Biology* **17**, e1008873 (2021).

638.

Sheik Amamuddy, O., Bishop, N. T. & Tastan Bishop, Ö. [Improving fold resistance prediction of HIV-1 against protease and reverse transcriptase inhibitors using artificial neural networks](https://doi.org/10.1186/s12859-017-1782-x). *BMC Bioinformatics* **18**, 369 (2017).

639.

Beerenwinkel, N. *et al.* [Geno2pheno: Interpreting genotypic HIV drug resistance tests](https://doi.org/10.1109/5254.972080). *IEEE Intelligent Systems* **16**, 35–41 (2001).

640.

Riemenschneider, M., Hummel, T. & Heider, D. [SHIVA - a web application for drug resistance and tropism testing in HIV](https://doi.org/10.1186/s12859-016-1179-2). *BMC Bioinformatics* **17**, 314 (2016).

641.

Beerenwinkel, N. *et al.* [Diversity and complexity of HIV-1 drug resistance: A bioinformatics approach to predicting phenotype from genotype](https://doi.org/10.1073/pnas.112177799). *Pnas* **99**, 8271–8276 (2002).

642.

Heider, D., Senge, R., Cheng, W. & Hüllermeier, E. [Multilabel classification for exploiting cross-resistance information in HIV-1 drug resistance prediction](https://doi.org/10.1093/bioinformatics/btt331). *Bioinformatics* **29**, 1946–1952 (2013).

---

[^1]: When the anti-HIV therapy starts clinicians use first-line drug regimens, if this treatment is changed due to resistance emergence then the second-line regimen is used.

[^2]: This sections build upon a review I participated in during my PhD <sup><a href="#ref-blasselDrugResistanceMutations2021" role="doc-biblioref">606</a></sup>