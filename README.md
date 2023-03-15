# Master Thesis
![](http://i.imgur.com/NdTFZRL.png) 
# Prediction of material parameters for numerical simulation through neural networks
In this master thesis, a method is developed to use machine learning to predict the
parameters for the material models in numerical simulation. Through deep neural
networks, it is possible to learn non-linear relationships between a set of input
values, known as training data, and the corresponding output, known as labels.
So, in a first step, to generate training data numerous tensile tests are simulated
which differ in terms of the elastic modulus, the Poisson’s ratio, and the shape of
the hardening curve. Here, an approach according to Hockett-Sherby was used to
describe the hardening curve, which provides 4 parameters for defining the shape.
MAT_24 is used as the material model for the numerical simulation. The selection
of the different parameters for this model is taken for thermoplastic polymers in
the reasonable range. In addition, all initial and boundary conditions as well as all
other assumptions and simulation settings must be the same for all virtual tensile
tests. The creation of material cards as well as the calculation of the virtual tests
in FE and the evaluation of these tests was automated with the scripting language
Python. The data resulting from the virtual tests, the force, and the strain field,
represent the training data for machine learning. The different parameters are also
used as labels. Various neural networks are trained using supervised learning to
ultimately predict the material parameters for the material model. In a convolutional
neural network CNN, the training data is interpreted as images. In this
connection, the force, X-direction displacement, and Y-direction displacement resulting
from the virtual tensile tests are precisely assumed to be the three channels
of colors in an RGB image. These neural networks have a better prognosis quality
than a recurrent neural network RNN. At the end of this work, real test data will
also be used to find a parameter set for real thermoplastic polymers using ML.

# Masterarbeit
# Vorhersage von Materialparametern für die numerische Simulation durch Neuronale Netze
In der vorliegenden Masterarbeit wird eine Methodik entwickelt, um maschinelles
Lernen zur Prognose der Parameter für Materialmodelle in numerische Simulation
einzusetzen. Durch tiefe neuronale Netze kann ein maschineller Lernalgorithmus
nichtlineare Beziehungen zwischen einem Satz von Eingabewerten, die als Inputs
bekannt sind, und der entsprechenden Ausgabe, die als Labels bekannt sind, lernen.
Zur Generierung von Trainingsdaten werden in einem ersten Schritt eine Vielzahl
von Zugversuchen simuliert, die sich in dem Elastizitätsmodul, der Poissonzahl
und der Form der Fließkurve unterscheiden. Hierfür wurde zur Beschreibung der
Fließkurve ein Ansatz nach Hockett-Sherby verwendet, der 4 Parameter zur Definition
der Form vorsieht. Als Materialmodell für die numerische Simulation wird das
MAT_24 verwendet. Die Auswahl der unterschiedlichen Parameter für dieses Modell
wird für einen spritzgegossenen Kunststoff im sinnvollen Bereich genommen.
Jedoch müssen alle Anfangs- und Randbedingungen sowie alle anderen Annahmen
und Simulationseinstellungen für alle virtuellen Zugversuche gleich sein. Die Erstellung
von generischen Materialkarten sowie die Berechnung von den virtuellen
Versuchen in FE und die Auswertung dieser Versuche werden mit der Skriptsprache
Python automatisiert. Nun stellen die aus den virtuellen Versuchen resultierten
Daten der Kraft und des Dehnungsfeldes die Trainingsdaten für das maschinelle
Lernen dar. Auf der anderen Seite werden die unterschiedlichen Parameter als
Labels verwendet. Verschiedene neuronale Netze werden mittels Supervised Learning
trainiert, um am Ende die Materialparameter für das Materialmodell zu prognostizieren.
Bei einem Convolutional Neural Network werden die Trainingsdaten
als Bilder interpretiert. In diesem Zusammenhang werden die aus den virtuellen
Zugversuchen resultierende Kraft, die Verschiebung in X-Richtung und die Verschiebung
in Y-Richtung genau als die drei Kanäle der Farben in einem RGB-Bild
angenommen. Diese neuronalen Netze weisen eine bessere Prognosegüte als bei
einem Recurrent Neural Network auf. Am Ende dieser Arbeit werden auch reale
Versuchsdaten verwendet, um einen Parametersatz für einen experimentell getesteten
Kunststoff mittels neuronaler Netze zu finden.
