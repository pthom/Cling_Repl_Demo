````cpp

// this will load the file init.cpp :
// - set some include and library paths
// - load opencv libraries
// - include opencv main files
// - include fplus
.L init.cpp

// this will load an image, and show it immediately
cv::Mat lena = cv::imread("lena.jpg");
cv::imshow("lena", lena); cv::waitKey(100);

// let's try some image manipulation
cv::Mat blur;
cv::blur(lena, blur, cv::Size(15, 15));
cv::imshow("blur", blur); cv::waitKey(100);

````