const API = {
  GetChatbotResponse: async (message) => {
    return new Promise(async (resolve, reject) => {
      try {
        if (message === "hi") {
          resolve("Welcome to TourLanka. A chatbot providing scholarly information about the importance and history of Sri Lanka tourist destinations.!");
        } else {
          console.log("Fetching data")
              const response = await fetch(`http://127.0.0.1:8000/?query=${encodeURIComponent(message)}`);
              const data = await response.json();  // ✅ Convert response to JSON
              console.log(data)
              return data.response;  // ✅ Extract 'response' field
        }
      } catch (error) {
        reject("Error communicating with the chatbot API: " + error.message);
      }
    });
  }
};

export default API;
