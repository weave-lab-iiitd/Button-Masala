#include "ofApp.h"
#include "ofAppGlutWindow.h"
#include "ofMain.h"

//--------------------------------------------------------------
int main(){
    // create a window
	// set width, height, mode (OF_WINDOW or OF_FULLSCREEN)
	ofSetupOpenGL(1024, 768, OF_WINDOW);
	ofRunApp(new ofApp()); // start the app
}
