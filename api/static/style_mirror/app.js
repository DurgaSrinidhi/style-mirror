/* =========================================================
   STYLE MIRROR - APP.JS
   ========================================================= */


/* =========================================================
   API
   ========================================================= */

const API_BASE = "/api";


/* =========================================================
   SUPABASE
   ========================================================= */

const SUPABASE_URL =
    "https://adturtkvwkaskwrrgemo.supabase.co";

/*
   IMPORTANT:
   Paste your existing Supabase PUBLISHABLE key here.

   Do NOT use a secret/service-role key.
*/

const SUPABASE_PUBLISHABLE_KEY =
    "sb_publishable_0DV2xEqWv6qmPFOjQNf_ww_ftFbvsZ-";


const supabaseClient =
    window.supabase.createClient(
        SUPABASE_URL,
        SUPABASE_PUBLISHABLE_KEY
    );


/* =========================================================
   APPLICATION STATE
   ========================================================= */

let accessToken = null;
let currentUser = null;
let currentProfileId = null;
let currentProjectId = null;
let currentProfile = null;


/* =========================================================
   ELEMENTS
   ========================================================= */

const authScreen =
    document.getElementById("authScreen");

const appContent =
    document.getElementById("appContent");


const loginTab =
    document.getElementById("loginTab");

const signupTab =
    document.getElementById("signupTab");


const nameGroup =
    document.getElementById("nameGroup");

const nameInput =
    document.getElementById("authName");


const emailInput =
    document.getElementById("authEmail");

const passwordInput =
    document.getElementById("authPassword");


const authForm =
    document.getElementById("authForm");

const authButton =
    document.getElementById("authButton");

const authMessage =
    document.getElementById("authMessage");


const logoutButton =
    document.getElementById("logoutButton");


const referenceImage =
    document.getElementById("referenceImage");

const originalImage =
    document.getElementById("originalImage");


const referenceFileName =
    document.getElementById("referenceFileName");

const originalFileName =
    document.getElementById("originalFileName");


const generateButton =
    document.getElementById("generateButton");


const statusElement =
    document.getElementById("status");


const resultSection =
    document.getElementById("resultSection");


const originalPreview =
    document.getElementById("originalPreview");

const editedPreview =
    document.getElementById("editedPreview");


const originalEmpty =
    document.getElementById("originalEmpty");

const editedEmpty =
    document.getElementById("editedEmpty");


const regenerateButton =
    document.getElementById("regenerateButton");

const exportButton =
    document.getElementById("exportButton");


const historyContainer =
    document.getElementById("historyContainer");


/* =========================================================
   AUTH MODE
   ========================================================= */

let authMode = "login";


function showLogin() {

    authMode = "login";


    if (loginTab) {
        loginTab.classList.add("active");
    }


    if (signupTab) {
        signupTab.classList.remove("active");
    }


    if (nameGroup) {
        nameGroup.classList.add("hidden");
    }


    if (authButton) {
        authButton.textContent = "Login";
    }


    if (authMessage) {
        authMessage.textContent = "";
    }

}


function showSignup() {

    authMode = "signup";


    if (signupTab) {
        signupTab.classList.add("active");
    }


    if (loginTab) {
        loginTab.classList.remove("active");
    }


    if (nameGroup) {
        nameGroup.classList.remove("hidden");
    }


    if (authButton) {
        authButton.textContent = "Sign Up";
    }


    if (authMessage) {
        authMessage.textContent = "";
    }

}


/* =========================================================
   AUTH TABS
   ========================================================= */

if (loginTab) {

    loginTab.addEventListener(
        "click",
        function (event) {

            event.preventDefault();

            showLogin();

        }
    );

}


if (signupTab) {

    signupTab.addEventListener(
        "click",
        function (event) {

            event.preventDefault();

            showSignup();

        }
    );

}


/* =========================================================
   AUTHENTICATION
   ========================================================= */

async function handleAuthentication(event) {

    if (event) {
        event.preventDefault();
    }


    const email =
        emailInput
            ? emailInput.value.trim()
            : "";


    const password =
        passwordInput
            ? passwordInput.value
            : "";


    const name =
        nameInput
            ? nameInput.value.trim()
            : "";


    if (!email) {

        authMessage.textContent =
            "Please enter your email.";

        return;
    }


    if (!password) {

        authMessage.textContent =
            "Please enter your password.";

        return;
    }


    if (password.length < 6) {

        authMessage.textContent =
            "Password must be at least 6 characters.";

        return;
    }


    if (authButton) {

        authButton.disabled = true;

        authButton.textContent =
            authMode === "signup"
                ? "Creating account..."
                : "Logging in...";
    }


    if (authMessage) {
        authMessage.textContent = "";
    }


    try {

        /* =====================================================
           SIGN UP
           ===================================================== */

        if (authMode === "signup") {

            if (!name) {

                throw new Error(
                    "Please enter your name."
                );

            }


            const {
                data,
                error
            } =
                await supabaseClient.auth.signUp({

                    email: email,

                    password: password,

                    options: {

                        data: {
                            name: name
                        }

                    }

                });


            if (error) {
                throw error;
            }


            console.log(
                "SIGN UP RESPONSE:",
                data
            );


            if (data.session) {

                accessToken =
                    data.session.access_token;

                currentUser =
                    data.session.user;


                await createOrLoadUserProfile();


                showApplication();

                return;
            }


            showLogin();


            if (emailInput) {
                emailInput.value = email;
            }


            if (passwordInput) {
                passwordInput.value = "";
            }


            if (authMessage) {

                authMessage.textContent =
                    "Account created successfully. You can now login.";

            }


            return;
        }


        /* =====================================================
           LOGIN
           ===================================================== */

        console.log(
            "Attempting Supabase login..."
        );


        const {
            data,
            error
        } =
            await supabaseClient.auth.signInWithPassword({

                email: email,

                password: password

            });


        console.log(
            "LOGIN RESPONSE:",
            data
        );


        if (error) {
            throw error;
        }


        if (!data || !data.session) {

            throw new Error(
                "Login completed but no session was returned."
            );

        }


        accessToken =
            data.session.access_token;

        currentUser =
            data.session.user;


        console.log(
            "LOGIN SUCCESS:",
            currentUser.email
        );


        await createOrLoadUserProfile();


        showApplication();

    }

    catch (error) {

        console.error(
            "AUTHENTICATION ERROR:",
            error
        );


        if (authMessage) {

            authMessage.textContent =
                error.message ||
                "Login failed.";

        }

    }

    finally {

        if (authButton) {

            authButton.disabled = false;

            authButton.textContent =
                authMode === "signup"
                    ? "Sign Up"
                    : "Login";

        }

    }

}


/* =========================================================
   AUTH BUTTON
   ========================================================= */

if (authButton) {

    authButton.type = "button";


    authButton.addEventListener(
        "click",
        handleAuthentication
    );

}


if (authForm) {

    authForm.addEventListener(
        "submit",
        function (event) {

            event.preventDefault();

        }
    );

}


/* =========================================================
   LOGOUT
   ========================================================= */

if (logoutButton) {

    logoutButton.addEventListener(
        "click",
        async function () {

            try {

                await supabaseClient.auth.signOut();

            }

            catch (error) {

                console.error(
                    "Logout error:",
                    error
                );

            }


            accessToken = null;

            currentUser = null;

            currentProfileId = null;

            currentProjectId = null;

            currentProfile = null;


            if (appContent) {
                appContent.classList.add("hidden");
            }


            if (authScreen) {
                authScreen.classList.remove("hidden");
            }


            showLogin();

        }
    );

}


/* =========================================================
   SUPABASE AUTH STATE
   ========================================================= */

supabaseClient.auth.onAuthStateChange(
    function (event, session) {

        console.log(
            "AUTH STATE:",
            event
        );


        if (session) {

            accessToken =
                session.access_token;

            currentUser =
                session.user;

        }

        else {

            accessToken = null;

            currentUser = null;

        }

    }
);


/* =========================================================
   USER PROFILE
   ========================================================= */

async function createOrLoadUserProfile() {

    if (!accessToken) {
        return;
    }


    try {

        const response =
            await fetch(
                `${API_BASE}/users/`,
                {

                    method: "GET",

                    headers: {

                        "Authorization":
                            `Bearer ${accessToken}`,

                        "Content-Type":
                            "application/json"

                    }

                }
            );


        if (!response.ok) {

            const text =
                await response.text();

            console.error(
                "User profile request failed:",
                text
            );

            return;
        }


        const data =
            await response.json();


        console.log(
            "USER PROFILE:",
            data
        );


        if (
            Array.isArray(data) &&
            data.length > 0
        ) {

            currentProfileId =
                data[0].id;

        }

        else if (
            data.results &&
            data.results.length > 0
        ) {

            currentProfileId =
                data.results[0].id;

        }

    }

    catch (error) {

        console.error(
            "Profile loading error:",
            error
        );

    }

}


/* =========================================================
   SHOW APPLICATION
   ========================================================= */

function showApplication() {

    console.log(
        "Opening STYLE MIRROR..."
    );


    if (authScreen) {
        authScreen.classList.add("hidden");
    }


    if (appContent) {
        appContent.classList.remove("hidden");
    }


    loadHistory();

}


/* =========================================================
   FILE NAME DISPLAY
   ========================================================= */

if (referenceImage) {

    referenceImage.addEventListener(
        "change",
        function () {

            if (
                referenceImage.files &&
                referenceImage.files.length > 0
            ) {

                referenceFileName.textContent =
                    referenceImage.files[0].name;

            }

        }
    );

}


if (originalImage) {

    originalImage.addEventListener(
        "change",
        function () {

            if (
                originalImage.files &&
                originalImage.files.length > 0
            ) {

                originalFileName.textContent =
                    originalImage.files[0].name;

            }

        }
    );

}


/* =========================================================
   API HELPER
   ========================================================= */

async function apiRequest(
    url,
    options = {}
) {

    options.headers =
        options.headers || {};


    if (accessToken) {

        options.headers["Authorization"] =
            `Bearer ${accessToken}`;

    }


    const response =
        await fetch(
            url,
            options
        );


    if (!response.ok) {

        const text =
            await response.text();


        console.error(
            "API ERROR:",
            response.status,
            url,
            text
        );


        throw new Error(
            `Request failed: ${response.status}`
        );

    }


    return response.json();

}


/* =========================================================
   GENERATE STYLE
   ========================================================= */

if (generateButton) {

    generateButton.addEventListener(
        "click",
        async function () {

            if (!accessToken) {

                setStatus(
                    "Please login first."
                );

                return;

            }


            if (
                !referenceImage ||
                !referenceImage.files.length
            ) {

                setStatus(
                    "Please select a reference image."
                );

                return;

            }


            if (
                !originalImage ||
                !originalImage.files.length
            ) {

                setStatus(
                    "Please select your original image."
                );

                return;

            }


            try {

                generateButton.disabled = true;


                /* =================================================
                   STEP 1 - GENERATE STYLE PROFILE
                   ================================================= */

                setStatus(
                    "Analyzing your reference image..."
                );


                const styleForm =
                    new FormData();


                styleForm.append(
                    "image",
                    referenceImage.files[0]
                );


                console.log(
                    "Calling:",
                    `${API_BASE}/generate-style-profile/`
                );


                const styleResponse =
                    await apiRequest(
                        `${API_BASE}/generate-style-profile/`,
                        {

                            method: "POST",

                            body: styleForm

                        }
                    );


                console.log(
                    "STYLE PROFILE RESPONSE:",
                    styleResponse
                );


                currentProfileId =
                    styleResponse.profile_id;


                currentProfile =
                    styleResponse.style;


                if (!currentProfileId) {

                    throw new Error(
                        "Style profile was not created."
                    );

                }


                /* =================================================
                   STEP 2 - UPLOAD ORIGINAL IMAGE
                   ================================================= */

                setStatus(
                    "Uploading your original image..."
                );


                const uploadForm =
                    new FormData();


                uploadForm.append(
                    "image",
                    originalImage.files[0]
                );


                uploadForm.append(
                    "image_type",
                    "original"
                );


                console.log(
                    "Calling:",
                    `${API_BASE}/uploaded-images/`
                );


                const uploadResponse =
                    await apiRequest(
                        `${API_BASE}/uploaded-images/`,
                        {

                            method: "POST",

                            body: uploadForm

                        }
                    );


                console.log(
                    "UPLOAD RESPONSE:",
                    uploadResponse
                );


                if (!uploadResponse.image) {

                    throw new Error(
                        "Original image upload failed."
                    );

                }


                /* =================================================
                   STEP 3 - CREATE PROJECT
                   ================================================= */

                setStatus(
                    "Creating your editing project..."
                );


                const projectResponse =
                    await apiRequest(
                        `${API_BASE}/projects/`,
                        {

                            method: "POST",

                            headers: {

                                "Content-Type":
                                    "application/json"

                            },

                            body:
                                JSON.stringify({

                                    name:
                                        "STYLE MIRROR Project",

                                    original_image_url:
                                        getAbsoluteUrl(
                                            uploadResponse.image
                                        ),

                                    editing_profile:
                                        currentProfileId

                                })

                        }
                    );


                console.log(
                    "PROJECT RESPONSE:",
                    projectResponse
                );


                currentProjectId =
                    projectResponse.id;


                if (!currentProjectId) {

                    throw new Error(
                        "Project was not created."
                    );

                }


                /* =================================================
                   STEP 4 - APPLY STYLE
                   ================================================= */

                setStatus(
                    "Applying the reference style..."
                );


                console.log(
                    "Calling:",
                    `${API_BASE}/apply-style/`
                );


                const applyResponse =
                    await apiRequest(
                        `${API_BASE}/apply-style/`,
                        {

                            method: "POST",

                            headers: {

                                "Content-Type":
                                    "application/json"

                            },

                            body:
                                JSON.stringify({

                                    profile_id:
                                        currentProfileId,

                                    project_id:
                                        currentProjectId

                                })

                        }
                    );


                console.log(
                    "APPLY STYLE RESPONSE:",
                    applyResponse
                );


                if (
                    !applyResponse.edited_image_url
                ) {

                    throw new Error(
                        "Edited image was not generated."
                    );

                }


                /* =================================================
                   STEP 5 - SHOW RESULT
                   ================================================= */

                showResult(
                    applyResponse.edited_image_url
                );


                showStyleParameters(
                    currentProfile
                );


                setStatus(
                    "Your STYLE MIRROR edit is ready!"
                );


                loadHistory();

            }

            catch (error) {

                console.error(
                    "GENERATE ERROR:",
                    error
                );


                setStatus(
                    "Generating failed: " +
                    error.message
                );

            }

            finally {

                generateButton.disabled =
                    false;

            }

        }
    );

}


/* =========================================================
   SHOW RESULT
   ========================================================= */

function showResult(url) {

    if (!resultSection) {
        return;
    }


    resultSection.classList.remove(
        "hidden"
    );


    if (
        originalPreview &&
        originalImage &&
        originalImage.files.length
    ) {

        originalPreview.src =
            URL.createObjectURL(
                originalImage.files[0]
            );


        originalPreview.classList.remove(
            "hidden"
        );

    }


    if (originalEmpty) {

        originalEmpty.classList.add(
            "hidden"
        );

    }


    if (editedPreview) {

        editedPreview.src =
            getAbsoluteUrl(url);


        editedPreview.classList.remove(
            "hidden"
        );

    }


    if (editedEmpty) {

        editedEmpty.classList.add(
            "hidden"
        );

    }

}


/* =========================================================
   STYLE PARAMETERS
   ========================================================= */

function showStyleParameters(style) {

    if (!style) {
        return;
    }


    console.log(
        "STYLE PARAMETERS:",
        style
    );


    const actualStyle =
        style.style || style;


    setValue(
        "lightness",
        actualStyle.lightness
    );


    setValue(
        "contrast",
        actualStyle.contrast
    );


    setValue(
        "warmth",
        actualStyle.warmth
    );


    setValue(
        "saturation",
        actualStyle.saturation
    );


    setValue(
        "highlight",
        actualStyle.highlight
    );


    setValue(
        "shadow",
        actualStyle.shadow
    );

}


/* =========================================================
   SET STYLE VALUE
   ========================================================= */

function setValue(id, value) {

    const element =
        document.getElementById(id);


    if (!element) {

        console.warn(
            "Style value element not found:",
            id
        );

        return;

    }


    if (
        value === undefined ||
        value === null ||
        value === ""
    ) {

        element.textContent = "—";

        return;

    }


    const numberValue =
        Number(value);


    if (
        Number.isFinite(numberValue)
    ) {

        element.textContent =
            Number.isInteger(numberValue)
                ? String(numberValue)
                : numberValue.toFixed(2);

    }

    else {

        element.textContent =
            String(value);

    }

}


/* =========================================================
   REGENERATE
   ========================================================= */

if (regenerateButton) {

    regenerateButton.addEventListener(
        "click",
        async function () {

            if (!currentProjectId) {

                setStatus(
                    "No project is available."
                );

                return;

            }


            try {

                regenerateButton.disabled =
                    true;


                setStatus(
                    "Regenerating your image..."
                );


                const response =
                    await apiRequest(
                        `${API_BASE}/projects/${currentProjectId}/regenerate/`,
                        {

                            method: "POST"

                        }
                    );


                console.log(
                    "REGENERATE RESPONSE:",
                    response
                );


                showResult(
                    response.image_url
                );


                setStatus(
                    "Regeneration complete!"
                );


                loadHistory();

            }

            catch (error) {

                console.error(
                    "Regeneration error:",
                    error
                );


                setStatus(
                    "Regeneration failed: " +
                    error.message
                );

            }

            finally {

                regenerateButton.disabled =
                    false;

            }

        }
    );

}


/* =========================================================
   EXPORT
   ========================================================= */

if (exportButton) {

    exportButton.addEventListener(
        "click",
        async function () {

            if (!currentProjectId) {

                setStatus(
                    "No project is available."
                );

                return;

            }


            try {

                exportButton.disabled =
                    true;


                setStatus(
                    "Exporting your image..."
                );


                const imageUrl =
                    editedPreview
                        ? editedPreview.src
                        : "";


                const response =
                    await apiRequest(
                        `${API_BASE}/exports/`,
                        {

                            method: "POST",

                            headers: {

                                "Content-Type":
                                    "application/json"

                            },

                            body:
                                JSON.stringify({

                                    project:
                                        currentProjectId,

                                    file_url:
                                        imageUrl,

                                    file_type:
                                        "jpg"

                                })

                        }
                    );


                console.log(
                    "EXPORT RESPONSE:",
                    response
                );


                const exportedUrl =
                    getAbsoluteUrl(
                        response.file_url
                    );


                setStatus(
                    "Image exported successfully!"
                );


                /*
                   Try to download the image instead
                   of opening it in a new tab.
                */

                try {

                    const imageResponse =
                        await fetch(
                            exportedUrl
                        );


                    if (!imageResponse.ok) {

                        throw new Error(
                            "Image download failed."
                        );

                    }


                    const imageBlob =
                        await imageResponse.blob();


                    const downloadUrl =
                        URL.createObjectURL(
                            imageBlob
                        );


                    const downloadLink =
                        document.createElement(
                            "a"
                        );


                    downloadLink.href =
                        downloadUrl;


                    downloadLink.download =
                        "style-mirror-edited-image.jpg";


                    downloadLink.style.display =
                        "none";


                    document.body.appendChild(
                        downloadLink
                    );


                    downloadLink.click();


                    document.body.removeChild(
                        downloadLink
                    );


                    setTimeout(
                        function () {

                            URL.revokeObjectURL(
                                downloadUrl
                            );

                        },
                        2000
                    );


                    setStatus(
                        "Image saved successfully!"
                    );

                }

                catch (downloadError) {

                    console.error(
                        "Download error:",
                        downloadError
                    );


                    /*
                       On phones, use the Share/Save sheet
                       when browser download is blocked.
                    */

                    if (
                        navigator.share &&
                        typeof File !== "undefined"
                    ) {

                        try {

                            const imageResponse =
                                await fetch(
                                    exportedUrl
                                );


                            const imageBlob =
                                await imageResponse.blob();


                            const imageFile =
                                new File(
                                    [imageBlob],
                                    "style-mirror-edited-image.jpg",
                                    {
                                        type:
                                            imageBlob.type ||
                                            "image/jpeg"
                                    }
                                );


                            if (
                                navigator.canShare &&
                                navigator.canShare({
                                    files: [imageFile]
                                })
                            ) {

                                await navigator.share({

                                    title:
                                        "STYLE MIRROR",

                                    text:
                                        "Edited image from STYLE MIRROR",

                                    files:
                                        [imageFile]

                                });


                                setStatus(
                                    "Image ready to save/share!"
                                );

                            }

                            else {

                                setStatus(
                                    "Please use the browser download option."
                                );

                            }

                        }

                        catch (shareError) {

                            console.error(
                                "Share error:",
                                shareError
                            );


                            setStatus(
                                "Please open the exported image and save it."
                            );

                        }

                    }

                    else {

                        setStatus(
                            "Please open the exported image and save it."
                        );

                    }

                }

            }

            catch (error) {

                console.error(
                    "Export error:",
                    error
                );


                setStatus(
                    "Export failed: " +
                    error.message
                );

            }

            finally {

                exportButton.disabled =
                    false;

            }

        }
    );

}


/* =========================================================
   HISTORY
   ========================================================= */

async function loadHistory() {

    if (!accessToken) {
        return;
    }


    if (!historyContainer) {
        return;
    }


    try {

        const response =
            await apiRequest(
                `${API_BASE}/history/`
            );


        const projects =
            response.projects || [];


        if (!projects.length) {

            historyContainer.innerHTML =
                "<p>No editing history yet.</p>";

            return;

        }


        historyContainer.innerHTML =
            "";


        projects.forEach(
            function (project) {

                const item =
                    document.createElement(
                        "div"
                    );


                item.className =
                    "history-item";


                const title =
                    document.createElement(
                        "h3"
                    );


                title.textContent =
                    project.name ||
                    "STYLE MIRROR Project";


                item.appendChild(
                    title
                );


                if (
                    project.edited_image_url
                ) {

                    const image =
                        document.createElement(
                            "img"
                        );


                    image.src =
                        getAbsoluteUrl(
                            project.edited_image_url
                        );


                    image.alt =
                        "Edited image";


                    item.appendChild(
                        image
                    );

                }


                historyContainer.appendChild(
                    item
                );

            }
        );

    }

    catch (error) {

        console.error(
            "History error:",
            error
        );

    }

}


/* =========================================================
   STATUS
   ========================================================= */

function setStatus(message) {

    if (statusElement) {

        statusElement.textContent =
            message;

    }

}


/* =========================================================
   URL HELPER
   ========================================================= */

function getAbsoluteUrl(url) {

    if (!url) {
        return "";
    }


    if (
        url.startsWith("http://") ||
        url.startsWith("https://")
    ) {

        return url;

    }


    return (
        window.location.origin +
        (
            url.startsWith("/")
                ? url
                : "/" + url
        )
    );

}


/* =========================================================
   EXISTING SESSION
   ========================================================= */

async function checkExistingSession() {

    try {

        const {
            data,
            error
        } =
            await supabaseClient.auth.getSession();


        if (error) {
            throw error;
        }


        console.log(
            "EXISTING SESSION:",
            data.session
        );


        if (data.session) {

            accessToken =
                data.session.access_token;

            currentUser =
                data.session.user;


            await createOrLoadUserProfile();


            showApplication();

        }

        else {

            if (authScreen) {

                authScreen.classList.remove(
                    "hidden"
                );

            }


            if (appContent) {

                appContent.classList.add(
                    "hidden"
                );

            }


            showLogin();

        }

    }

    catch (error) {

        console.error(
            "Session error:",
            error
        );


        if (authScreen) {

            authScreen.classList.remove(
                "hidden"
            );

        }


        if (appContent) {

            appContent.classList.add(
                "hidden"
            );

        }

    }

}


/* =========================================================
   START APPLICATION
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        showLogin();

        checkExistingSession();

    }
);