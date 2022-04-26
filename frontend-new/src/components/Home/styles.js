
const styles = theme => ({
    root: {
        flexGrow: 1,
        minHeight: "100vh"
    },
    grow: {
        flexGrow: 1,
    },
    main: {

    },
    container: {
        flex: 1,
        flexDirection: 'row',
        backgroundColor: "#ffffff",
        paddingTop: "30px",
        paddingBottom: "20px",
    },
    containerDescription: {
        fontSize: "1.8rem",
        fontFamily: "Roboto, Helvetica, Arial, sans-serif",
        fontWeight: 500,
    },
    childContainer: {
        flex: 0.5,
        flexDirection: 'row',
        backgroundColor: "#ffffff",
        paddingTop: "30px",
        paddingBottom: "20px",
    },
    dropzone: {
        flex: 1,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        margin: "20px",
        borderWidth: "2px",
        borderRadius: "2px",
        borderColor: "#cccccc",
        borderStyle: "dashed",
        backgroundColor: "#fafafa",
        outline: "none",
        transition: "border .24s ease-in-out",
        cursor: "pointer",
        backgroundImage: "url(https://www.svgrepo.com/show/9443/photo-camera.svg)",
        backgroundRepeat: "no-repeat",
        backgroundPosition: "center",
        minHeight: "400px",
        backgroundSize: "30vh",
    },
    fileInput: {
        display: "none",
    },
    preview: {
        width: "100%",
        objectFit: "cover"
    },
    help: {
        fontSize: "40px",
        color: "#302f2f"
    },
    safe: {
        color: "#1C6331",

    },
    poisonous: {
        color: "#de2d26",
    },
    askContainer: {
        display: "flex",
        justifyContent: "center",
        alignItems: "left",
    },
    microphone: {
        width: "10vw",
        height: "7vh",
    },
    microphoneStatus: {
        fontSize: "20px",
    },
    microphoneTextInput: {
        fontSize: "1.3rem",
        height: "7vh",
        padding: "10px",
        borderWidth: "medium",
        borderRadius: "5px",
        borderColor: "black",
    },
    askButton: {
        height: "7vh",
        paddingTop: "15px",
        paddingBottom: "20px",
        paddingLeft: "20px",
        paddingRight: "20px",
        fontSize: "1.6rem",
        // marginLeft: "2vw",
        textAlign: "center",
        backgroundColor: "#A41034",
        color: "white", 
        fontWeight: 600,
        borderStyle: "hidden",
    },
    answerContainer: {
        display: "flex",
        justifyContent: "center",
        alignItems: "left",
        marginTop: "5vh"
    },
});

export default styles;