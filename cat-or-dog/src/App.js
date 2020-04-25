import React from "react";
import "./App.css";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      showCam: false,
      vidCap: null,
      hasSelected: false,
    };
    this.uploadChangeHandler = this.uploadChangeHandler.bind(this);
    this.cameraClickHandler = this.cameraClickHandler.bind(this);
    this.captureClickHandler = this.captureClickHandler.bind(this);
    this.verdictClickHandler = this.verdictClickHandler.bind(this);
    this.videoRef = React.createRef();
    this.captureRef = React.createRef();
  }

  // Activate or deactivate the camera, attach video stream to video element.
  async cameraClickHandler() {
    let { vidCap } = this.state;
    if (vidCap != null) {
      this.setState((prevState) => {
        const currState = !prevState.showCam;
        vidCap.getVideoTracks().forEach((track) => track.stop());
        return {
          showCam: currState,
          vidCap: null,
        };
      });
    } else {
      try {
        const constraints = { video: { facingMode: "environment", aspectRatio: 1 } };
        vidCap = await navigator.mediaDevices.getUserMedia(constraints);
        this.setState((prevState) => ({
          vidCap: vidCap,
          showCam: !prevState.showCam,
        }));
      } catch (err) {
        console.error(err);
      }
    }
  }

  // Grab file from user directory
  async uploadChangeHandler(e) {
    const { files } = e.target;
    if (files.length > 0) {
      const fr = new FileReader();
      fr.onload = (_e) => {
        const image = new Image();
        image.onload = (_e) => {
          const { width: imageWidth, height: imageHeight } = image;
          // Center crop the image
          const size = imageHeight < imageWidth ? imageHeight : imageWidth;
          const sx = Math.max((imageWidth - imageHeight) / 2, 0);
          const sy = Math.max((imageHeight - imageWidth) / 2, 0);

          const { width, height } = this.captureRef.current;
          this.captureRef.current.getContext("2d").drawImage(image, sx, sy, size, size, 0, 0, width, height);
          this.setState({ hasSelected: true });
        };
        image.src = fr.result;
      };
      fr.readAsDataURL(files[0]);
    }
  }

  // Capture image onto canvas when capture is clicked.
  captureClickHandler(e) {
    console.log("...klachic");
    const { width, height } = this.captureRef.current;
    this.captureRef.current.getContext("2d").drawImage(this.videoRef.current, 0, 0, width, height);
    this.setState({ hasSelected: true });
  }

  verdictClickHandler() {
    // const { width, height } = this.captureRef.current;
    const { current: canvas } = this.captureRef;
    let link = document.createElement("a");
    link.download = "filename.png";
    link.href = canvas.toDataURL();
    link.click();
  }

  render() {
    const { showCam, vidCap, hasSelected } = this.state;
    const { innerWidth, innerHeight } = window;

    const size = innerWidth > innerHeight ? "50vh" : "90vw";
    const marginBottom = showCam ? "24px" : "0px";

    const shouldShowVideo = showCam ? size : "0";
    const shouldShowCanvas = showCam ? `calc(${size}/3)` : hasSelected ? size : "0";

    if (vidCap != null && showCam) {
      this.videoRef.current.srcObject = vidCap;
    }

    const titleStyle = { marginTop: showCam ? "0" : "-15vh" };
    const videoStyle = { height: shouldShowVideo, width: shouldShowVideo, marginBottom };
    const canvasStyle = { marginBottom: hasSelected ? "24px" : marginBottom, height: shouldShowCanvas, width: shouldShowCanvas };
    return (
      <div className="App">
        <h1 className="App-title" style={titleStyle}>
          <span className="App-title-hp">Cat</span> <span className="App-title-or">or</span> <span className="App-title-hp">Dog</span>
        </h1>
        <video ref={this.videoRef} style={videoStyle} className="Video" autoPlay></video>
        <canvas ref={this.captureRef} style={canvasStyle} className="Canvas" width="224" height="224"></canvas>
        <div className="Button-container">
          {hasSelected && (
            <button className="Button" id="Button-click" onClick={this.verdictClickHandler}>
              Verdict
            </button>
          )}
          {showCam ? (
            <button className="Button" id="Button-click" onClick={this.captureClickHandler}>
              Capture
            </button>
          ) : (
            <label className="Button" id="Button-upload">
              <input type="file" accept="image/*" style={{ display: "none" }} onChange={this.uploadChangeHandler} />
              Select
            </label>
          )}
          <button className="Button" id="Button-click" onClick={this.cameraClickHandler}>
            {showCam ? "Stop" : "Camera"}
          </button>
        </div>
      </div>
    );
  }
}

export default App;
