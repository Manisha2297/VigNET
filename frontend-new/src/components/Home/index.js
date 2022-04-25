import React, { useEffect, useRef, useState } from 'react';
import { withStyles } from '@material-ui/core';
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';
import SpeechRecognition, { useSpeechRecognition } from "react-speech-recognition";
import microPhoneIcon from "../../mic.svg"

import DataService from "../../services/DataService";
import styles from './styles';
import styled, { keyframes, css } from "styled-components";
// import {TextInput} from "react-native";
import { Oval, TailSpin } from  'react-loader-spinner';
import Say, {SayButton, SayUtterance} from 'react-say';
import imageCompression from 'browser-image-compression';
import { isChrome, isEdge, isFirefox, isSafari } from 'react-device-detect';

const colorBg = keyframes`0% {
    background-color: #fff;
}

50% {
    background-color: #cc4455;
}

100% {
    backgrouond-color: #fff;
}`
const animation = 
css`
${colorBg} 1.5s alternate ease-in-out infinite;
`
const MicrophoneIconElement = styled.img.attrs({
    src: microPhoneIcon,
    alt: "Click to ask a question"
})`animation: ${props=>props.active? animation : "none"};`

const Home = (props) => {
    const { classes } = props;
    const true_value = true;
    const false_value = false;

    const inputFile = useRef(null);

    // Component States
    const [image, setImage] = useState(null);
    const [prediction, setPrediction] = useState(null);
    const [isLoading, setLoading] = useState(false);


    const [error, setError] = useState(null);
    const errorDiv = error 
        ? <div className="error">
            <i class="material-icons error-icon">error_outline</i>
            {error}
          </div> 
        : '';


    // Setup Component
    useEffect(() => {

    }, []);

    useEffect(() => {

    }, []);

    // Handlers
    const handleImageUploadClick = () => {
        inputFile.current.click();
    }
    const handleOnChange = (event) => {
        setImage(URL.createObjectURL(event.target.files[0]));
        if(prediction){
          setPrediction(null);
        }
        if(isLoading){
          setLoading(!isLoading);
        }
        // var formData = new FormData();
        // formData.append("file", event.target.files[0]);
        // DataService.Predict(formData)
        //     .then(function (response) {
        //         console.log(response.data);
        //         setPrediction(response.data);
        //     })
    }

    const onSumbit = async () => {
        var formData = new FormData();
        if(transcript){
          formData.append("question", transcript);

        }
        else{
          formData.append("question", textInput);
        }
        const options = {
          maxSizeMB: 0.08,
          maxWidthOrHeight: 350,
          useWebWorker: true
        }
        const compressedFile = await imageCompression(inputFile.current.files[0], options);
        // console.log(compressedFile);
        // const compressedFile = inputFile.current.files[0];
        // console.log(inputFile.current.files[0]);
        formData.append("file", compressedFile);
        setLoading(!isLoading);
        DataService.Predict(formData)
            .then(function (response) {
                setPrediction(response.data);
                setLoading(!isLoading);
            })
            .catch(res => {
              console.log(res.error);
              setError(res.error);
              setLoading(!isLoading);

          })
    }

    const { transcript, resetTranscript } = useSpeechRecognition();
    var [isListening, setIsListening] = useState(false_value);
    var [isActive, setIsActive] = useState(false_value);
    var [textInput, setTextInput] = useState(transcript);
    const textRef = useRef(textInput); 

    const microphoneRef = useRef(null);
    if (!SpeechRecognition.browserSupportsSpeechRecognition()) {
      // return (
      //   <div className="mircophone-container">
      //     Browser does not Support Speech Recognition.
      //   </div>
      // );
      // setSpeechSupported(!isSpeechSupported);
      console.log("Speech not supported");

    }
    const isKeyEnter = (event) => {
      if(event.key=='Enter'){
        if(event.target.className.includes("microphone")){
          handleListing();
        }
        else if(event.target.className.includes("preview")){
          handleImageUploadClick();
        }
        else if(event.target.className.includes("askButton")){
          onSumbit();
        }
      }


    }
    const handleListing = () => {
      if(!isListening){
        resetTranscript();
        setPrediction(null);
        setLoading(false);
        setTextInput(null);
        microphoneRef.current.classList.add("listening");
        SpeechRecognition.startListening({
          continuous: true,
  
        });
      }
      else{
        microphoneRef.current.classList.remove("listening");
        SpeechRecognition.stopListening();
      }
      setIsListening(!isListening);
      setIsActive(!isActive);

    };

    const textHandleChange = (event) => {
      if(prediction){
        setPrediction(null);
      }
      if(isLoading){
        setLoading(!isLoading);
      }
      if(event.target.value){
        setTextInput(event.target.value);
        resetTranscript();
      }
      else {
        setTextInput(transcript);
      }
    }

    // const stopHandle = () => {
    //     setIsListening(false_value);
    //     setIsActive(false_value);
    //     console.log(isActive);
    //     console.log("Stopping");
    //     console.log(isListening);
    //     console.log(transcript);
    //     microphoneRef.current.classList.remove("listening");
    //     console.log(microphoneRef.current.classList);
    //     SpeechRecognition.stopListening();
    // };

 

    // const handleReset = () => {
    //   stopHandle();
    //   resetTranscript();
    // //   console.log(isListening);
    // //   console.log(isActive);
    // };


    

    return (
        <div className={classes.root}>
            <main className={classes.main}>
                <Container className={classes.container}>
                    <div>
                        <p className={classes.containerDescription}>
                            This application will help you understand the things around you just by clicking a picture of your surrounding and asking a question related to the picture. Please click on capture an image button and click on the microphone to ask your question. You will get an answer within seconds!
                          </p>
                    </div>
                    {/* {prediction &&
                        <Typography variant="h4" gutterBottom align='center'>
                            {!prediction.poisonous &&
                                <span className={classes.safe}>{prediction.prediction_label + " (" + prediction["accuracy"] + "%)"}</span>
                            }
                            {prediction.poisonous &&
                                <span className={classes.poisonous}>{prediction.prediction_label + " (" + prediction["accuracy"] + "%)"}&nbsp;&nbsp;Poisonous</span>
                            }
                        </Typography>
                    } */}
                    <div className={classes.dropzone} onClick={() => handleImageUploadClick()} onKeyDown={isKeyEnter} tabIndex="0">
                        <input
                            type="file"
                            accept="image/*"
                            capture="camera"
                            on
                            autocomplete="off"
                            className={classes.fileInput}
                            ref={inputFile}
                            onChange={(event) => handleOnChange(event)} 
                        />
                        <div><img className={classes.preview} src={image} tabIndex="0"/></div>
                        <div className={classes.help}>Click to take a picture or upload an image</div>
                    </div>
                </Container>
                <Container className={classes.childContainer}>
                <div className="microphone-wrapper">
      <div className="mircophone-container">
        </div>
        <div className={classes.askContainer}>
        {/* <span className={classes.microphoneStatus}>
          Click to ask a question
        </span> */}
        <span
          className={classes.microphoneIconContainer}
          ref={microphoneRef}
          onClick={handleListing}
          onKeyDown={isKeyEnter}
        >
        {/* <img src={microPhoneIcon} className="microphone-icon" /> */}
        {!isFirefox && <MicrophoneIconElement className={classes.microphone} active={isActive} tabIndex="0"></MicrophoneIconElement>}
      </span>
          <span className="microphone-result-text"><textarea className={classes.microphoneTextInput} defaultValue={transcript} required placeholder='Your question here' onChange={textHandleChange}></textarea></span>
          </div>
        <div className={classes.answerContainer}>
            <button className={classes.askButton} onClick={onSumbit} onKeyDown={isKeyEnter}>
            Get Answer
            </button>
        </div>

          <Container className={classes.childContainer}>

          {prediction ?
                        <Typography variant="h4" gutterBottom align='center'>
                                <span className={classes.safe}>{"Answer is " + prediction.prediction_label_vilt }</span>
                        </Typography>
                        : <>{isLoading ? (<span><TailSpin color="#A41034" height={80} width={700} alt="loading" style={{display: isLoading? 'block': 'none'}}/></span>): null}</>
                    }
                    </Container>
        {/* <div> */}

        {/* <span hidden={isLoading ? '': 'hidden'}>
          {isLoading && (<Oval color="#00BFFF" height={80} width={700} alt="loading" style={{display: isLoading? 'block': 'none'}}/>)}
          </span> */}
        {errorDiv}
        {prediction && (isChrome || isEdge || isFirefox) && <Say pitch={1.1} rate={1.0} volume={0.8} speak={prediction? prediction.prediction_label_vilt: ''} text={prediction? prediction.prediction_label_vilt: ''}/>
}
        {/* </div> */}
        {/* <div>
            {transcript && (
          <button className="microphone-reset btn" onClick={handleReset}>
            Reset
          </button>
          )}
        </div> */}
    </div>
                </Container>
            </main>
        </div>
    );

};



export default withStyles(styles)(Home);