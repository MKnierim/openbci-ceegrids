# openbci-ceegrids
This repository contains the description and materials for the implementation of a cEEGrid adapter for the use with the OpenBCI Cyton + Daisy biosignal acquisition boards.

<img src="./imgs/top_v1.jpg" alt="Adapted OpenBCI Cyton Enclosure with Slots for the cEEGrid Adapter Holder" height="250"/> <img src="./imgs/adapter_v1.jpg" alt="cEEGrid Adapter with Enclosure (Adapter Holder)" height="250"/>

<img src="./imgs/system_v1.jpg" alt="Complete OpenBCI-cEEGrid System" height="250"/> <img src="./imgs/bottom_v1.jpg" alt="Adapted OpenBCI Cyton Enclosure with Clip for Head-Worn Isolated Applications" height="250"/>

This repository contains:

1. [Bill of Materials (BOM)](#materials)
1. [3D-Print Files](./stl/)
1. [Assembly Instructions](#assembly-instructions)
1. [Technical Evaluation Documentation](./lit/technical_evaluation.pdf) - also available at [ArXiv](https://arxiv.org/abs/2102.00414)

Please take a look at the sections below and the other repository files for details.

For the documentation of the cEEGrid development please refer to the [cEEGrid developers website](http://ceegrid.com/) or the publication by [Debener et al. 2015](https://www.nature.com/articles/srep16743).

------

## Application Options
Currently, there are two main options for using the system:

1. Isolated Use: 18-channel head-worn cEEGrid data collection (wear it using a headband, basecap, or even with a VR headset)
2. Combined Use: Selective cEEGrid channel use in combination with selected OpenBCI Ultracortex MK IV scalp electrodes (use it for the exploration of interesting channel and reference combinations)

<img src="./imgs/use_case_1.jpg" alt="Isolated Use: Headband" height="250"/> <img src="./imgs/use_case_2.jpg" alt="Isolated Use: Basecap" height="250"/>

<img src="./imgs/use_case_3.jpg" alt="Isolated Use: VR Headset" height="250"/> <img src="./imgs/use_case_4.jpg" alt="Combined Use: Ultracortex MK IV" height="250"/>

------

## Known Use Cases
So far, the cEEGrids have demonstrated their ability to record typical EEG phenomena related to visual stimulation (posterior Alpha increases with reduced visual information - see [1]), to auditory stimulation (detection of directed speaker attention – see [2, 3, 4, 5]), sleep stage detection [6, 7, 8] and changes in mental workload in driving simulations [9]. Furthermore, there are first investigations being put forward that focus on the observation of human-computer-interaction use cases, for example the observation of flow experiences using the cEEGrids [10]. Related use cases like the observation of immersion or cognitive absorption depth (e.g. in VR scenarios) or general task engagement and difficulty could be possible but need to be researched further.

References:

1. Stefan Debener, Reiner Emkes, Maarten De Vos, and Martin Bleichner. 2015. Unobtrusive ambulatory EEG using a smartphone and flexible printed electrodes around the ear. Sci. Rep. 5, (2015), 1–11. DOI:https://doi.org/10.1038/srep16743
2. Markus Garrett, Stefan Debener, and Sarah Verhulst. 2019. Acquisition of subcortical auditory potentials with around-the-ear ceegrid technology in normal and hearing impaired listeners. Front. Neurosci. 13, JUL (2019), 1–15. DOI:https://doi.org/10.3389/fnins.2019.00730
3. Manuela Jaeger, Bojana Mirkovic, Martin G. Bleichner, and Stefan Debener. 2020. Decoding the Attended Speaker From EEG Using Adaptive Evaluation Intervals Captures Fluctuations in Attentional Listening. Front. Neurosci. 14, June (2020), 1–16. DOI:https://doi.org/10.3389/fnins.2020.00603
4. Bojana Mirkovic, Martin G Bleichner, Maarten De Vos, and Stefan Debener. 2016. Target Speaker Detection with Concealed EEG Around the Ear. Front. Neurosci. 10, July (2016), 1–11. DOI:https://doi.org/10.3389/fnins.2016.00349
5. Waldo Nogueira, Hanna Dolhopiatenko, Irina Schierholz, Andreas Büchner, Bojana Mirkovic, Martin G. Bleichner, and Stefan Debener. 2019. Decoding selective attention in normal hearing listeners and bilateral cochlear implant users with concealed ear EEG. Front. Neurosci. 13, JUL (2019), 1–15. DOI:https://doi.org/10.3389/fnins.2019.00720
6. Martin G. Bleichner and Stefan Debener. 2017. Concealed, unobtrusive ear-centered EEG acquisition: Ceegrids for transparent EEG. Front. Hum. Neurosci. 11, April (2017), 1–14. DOI:https://doi.org/10.3389/fnhum.2017.00163
7. Kaare B. Mikkelsen, James K. Ebajemito, Maria A. Bonmati-Carrion, Nayantara Santhi, Victoria L. Revell, Giuseppe Atzori, Ciro della Monica, Stefan Debener, Derk Jan Dijk, Annette Sterr, and Maarten de Vos. 2019. Machine-learning-derived sleep–wake staging from around-the-ear electroencephalogram outperforms manual scoring and actigraphy. J. Sleep Res. 28, 2 (2019). DOI:https://doi.org/10.1111/jsr.12786
8. Annette Sterr, James K. Ebajemito, Kaare B. Mikkelsen, Maria A. Bonmati-Carrion, Nayantara Santhi, Ciro della Monica, Lucinda Grainger, Giuseppe Atzori, Victoria Revell, Stefan Debener, Derk Jan Dijk, and Maarten DeVos. 2018. Sleep EEG derived from behind- the-ear electrodes (cEEGrid) compared to standard polysomnography: A proof of concept study. Front. Hum. Neurosci. 12, November (2018), 1–9. DOI:https://doi.org/10.3389/fnhum.2018.00452
9. Edmund Wascher, Stefan Arnau, Julian Elias Reiser, Georg Rudinger, Melanie Karthaus, G. Rinkenauer, F. Dreger, and Stephan Getzmann. 2019. Evaluating Mental Load During Realistic Driving Simulations by Means of Round the Ear Electrodes. Front. Neurosci. 13, September (2019), 1–11. DOI:https://doi.org/10.3389/fnins.2019.00940
10. Michael T. Knierim, Christoph Berger, Pierluigi Reali. 2020. Open-Source Concealed EEG Data Collection for Brain-Computer-Interfaces -- Real-World Neural Observation Through OpenBCI Amplifiers with Around-the-Ear cEEGrid Electrodes. ArXiv, (2020), 1-28. DOI:https://arxiv.org/abs/2102.00414


------

## Materials

| Amount | Part   Description                                                  | Instance /   Reference                                                                                               |
|--------|---------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------|
| 1      | OpenBCI Cyton Board + Daisy Shield   (Biosignal Acquisition Boards) | Available from the manufacturer at: https://shop.openbci.com/collections/frontpage/products/cyton-daisy-biosensing-boards-16-channel?variant=38959256526                                                                                  |
| 2      | cEEGrid Electrodes                                                  | Available from   the manufacturer at: https://shop.tmsi.com/product/ceegrid                                          |
| 2      | Printed   Circuit Boards                                            | Custom PCB made   available by the cEEGrid developers here: https://github.com/mgbleichner/nEEGlace/tree/master/cEEGrid-Adapter; Can be manufactured on demand, e.g. at https://aisler.net/ (upload all files as .zip)                                                                                                                                                                 |
| 1      | Re-designed Cyton + Daisy Board Mounts                              | [3D-Print Files](./stl/)                                                       |
| 2      | PCB Holder                                                          | [3D-Print Files](./stl/)                                                                                             |
| 1      | Headband Clip                                                       | [3D-Print Files](./stl/)                                                                                             |
| 2      | No. 4 Screws for Brittle Plastic                                    | To attach the headband clip to the   Cyton board mount - https://www.mcmaster.com/90385A323/                         |
| 2      | Mini Edge Card Socket                                               | SAMTEC MB1-120-01-L-S-01-SL-N –   configurable at https://www.samtec.com/products/mb1                                |
| 20     | Pin Headers                                                         | Here we used short male headers   with 0.1 inch pitch, e.g. available at https://www.adafruit.com/product/3009       |
| 20     | Jumper Cables                                                       | Here we used short (3 inch)   female/female jumper wires, e.g. available at   https://www.adafruit.com/product/1951  |

------

## Assembly Instructions
The herein described system is comprised of three main components: (1) The OpenBCI Cyton microcontroller with the Daisy shield that enables the low-cost mobile biosignal acquisition (e.g. EEG, ECG, or EMG), (2) the cEEGrid electrodes, a set of flexible printed Ag/AgCl electrodes in a c-shaped form that can be placed around a person’s ear using adhesives, and (3) the printed circuit board that transmits the signal from the applied cEEGrids to an amplifier. To assemble the system, please follow these instructions:

(1) For the OpenBCI Cyton+Daisy assembly for regular EEG data collection, please follow the thorough instructions provided by the device manufacturers: https://docs.openbci.com/docs/04AddOns/01- Headwear/MarkIV (Last accessed: September 13, 2020). In this documentation, the 3D printed parts are also provided. For the herein presented system to work, the regular board holder (or board mount) needs to be 3D-printed. Also, two #4 screws for brittle plastic are required to attach the clip that is mentioned in step (3). As a power supply, use a ~500mAh lithium-ion rechargeable battery pack that fits into the board holder.

(2) For the assembly of the cEEGrid adapter, we followed the instructions provided by the cEEGrid developers: http://ceegrid.com/home/how-to-connect/ (Last accessed: September 13, 2020 - see: https://web.archive.org/web/20190403064220/http://ceegrid.com/home/how-to-connect/). To assemble the adapter, three parts are required, a contact point that connects to the cEEGrid pins (2mm pitch – used here is a mini edge card socket by the company SAMTEC), a simple printed circuit board, and a set of male or female pin headers with 2.54mm pitch (double row). The parts can be joined using a soldering iron. To facilitate the soldering of the mini edge card socket to the PCB and to lower the risk of bridges it is recommended that every second pin (but starting with the first pin) of the card socket is removed before assembling the connector.

(3) Finally, to integrate the two initial components, a few additional steps and components need to be completed. For the herein shown system, a decision was made to solder on stack headers on to the PCB. Initially, individual jumper cables were soldered on to the PCB, yet were found to be a bit cumbersome to work with since not all of the cables can be used with the Cyton+Daisy boards (20 cables for 18 pins). Also, the stack headers provided more flexibility to adapt cable lengths for different mounting solutions. To link the cEEGrid PCB and the OpenBCI board, now only a set of 20 short female jumper cables is required. For this final assembly step, two important aspects need to be mentioned. First, the cables should be attached securely to reduce artefacts that might appear due to cable movement. We have opted for a simple solution of twisting the cables together to secure them. Second, care needs to be taken to route the cables to the recording pins on the OpenBCI board correctly. While the cEEGrid is symmetrical, the fact that two electrodes need to be left out in this configuration requires an adequate mapping for the left and right ear. To facilitate this step, the schematic below shows the pins on the cEEGrid for the left and right ear. We recommend connecting the right ear to the Cyton pins (channel 1-8 in the OpenBCI GUI) and the left ear to the Daisy pins (channel 9-16 in the OpenBCI GUI). We also recommend maintaining the colour coding to keep track of which electrodes are being used and which are left out. For the correct routing of the reference and ground electrodes, please refer to the OpenBCI documentation mentioned in step (1) or consider the placement of the grey cables in the schematic below. To complete the system, the two parts of the headband clip, the PCB holder, and the re-designed Cyton board cover need to be 3D-printed. Regular FDM printing can be used with a standard 0.4 mm nozzle diameter and 0.2 mm layer height. Rather slow print speeds (e.g. 40 mm/s) should be used as the parts have fine details. The clip can then be secured on the board holder by using the two #4 screws. The PCB holder can be attached without any additional material. First, the Daisy module should be lifted up. Then the PCB holder can be put in and clipped between the board cover and the Daisy module.

<img src="./imgs/mappings.png" alt="Schematic of the mapping of cEEGrid electrode channels on the PCB to the Cyton and Daisy pins, including a color-coding and channel reference as visible in the OpenBCI GUI during recording."/>
