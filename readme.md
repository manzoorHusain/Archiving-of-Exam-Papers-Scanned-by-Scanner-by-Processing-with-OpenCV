Bundan sonra çalışmalarımızı burdan yürüteceğiz. Herkes kendi branchta çalışacak ve hepimiz kolay bir şekilde herkesin yaptığı çalışmasını görebileceğiz.


After reading the exam image it gets splitted into two rectangles from top to bottom
then the program starts processing the QR code on the left hand side.
For QR code processing Pyzbar library is used.
https://github.com/prash29/Barcode-Reader/blob/master/barcode.py
the code in the link above is used to extract information stored inside our QR code.


Then the right hand side of the image gets processed.
First the box that contains the optic form is recognized using Contours.
To find the optic form the code in the link under is used.
https://answers.opencv.org/question/230784/finding-rectangle-contours-in-an-image/


After that the optic form gets processed.

Manzur you start explaining here please...
