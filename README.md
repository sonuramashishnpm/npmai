npmai

npmai (by Sonu Kumar Ramashish) is a lightweight Python package that seamlessly connects you  with Ollama and 10 other open-source models without any Installation, Login/Signup or API problems.

🚀 Features

Execute prompts on multiple LLMs simultaneously:["LLaMA-3.2","CodeLLaMA-Instruct 7B","Gemma-2-Instruct 9B","Mistral 7B Instruct","Qwen-2.5-Coder 7B","Phi-3 Medium (8B)","Falcon 7B Instruct","Baichuan-2-7B","InternLM-Chat-7B","Vicuna 7B"]

Fully LangChain,CrewAI and other -compatible interface.

Simple and intuitive invoke() for instant responses.

Support continuous conversation.

Encourages responsible usage.

#For documentation visit:- https://npmai.onrender.com

⚙️ Installation
pip install npmai


Tip: For Python 3.13, make sure to use:

py -3.13 -m pip install npmai

💡 How to Use

for Documentation visit:- https://npmai.netlify.app or https://npmai.onrender.com

Basic Examples
for Python:-

1.Import npmai Module
from npmai import Ollama

Initialize Ollama:

llm = Ollama()      

prompts=""

model="llama3.2" #you can keep other also

Invoke a prompt and get the response:

response = llm.invoke(prompts,model)
print(response) 

#If you want to use npmai through other languages consider hitting this api endpoint:-
https://npmai-api.onrender.com

example:-
with other languages
#Java Script-
async function callApi() {
  const payload = {
    prompt: "hey my name is sonu kumar what do you think about Narendra Modi",
    model: "llama3.2",
    temperature: 0.4,
  };

  const response = await fetch("https://npmai-api.onrender.com/llm", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  const data = await response.json();
  console.log(data.response);
}

callApi();

#C++
#include <httplib.h>
#include <nlohmann/json.hpp>
#include <iostream>

int main() {
    httplib::Client cli("https://npmai-api.onrender.com");
    nlohmann::json payload = {
        {"prompt", "hey my name is sonu kumar what do you think about Narendra Modi"},
        {"model", "llama3.2"},
        {"temperature", 0.4}
    };

    auto res = cli.Post("/llm", payload.dump(), "application/json");
    if (res) {
        auto data = nlohmann::json::parse(res->body);
        std::cout << data["response"] << std::endl;
    }
    return 0;
}

#Java
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class Main {
    public static void main(String[] args) throws Exception {
        String json = "{\"prompt\": \"hey my name is sonu kumar what do you think about Narendra Modi\", \"model\": \"llama3.2\", \"temperature\": 0.4}";
        
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("https://npmai-api.onrender.com/llm"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(json))
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        // Note: For simple output, print full body; for parsing, use a library like Jackson or Gson
        System.out.println(response.body());
    }
}

#C
#include <stdio.h>
#include <curl/curl.h>

int main(void) {
    CURL *curl = curl_easy_init();
    if(curl) {
        struct curl_slist *headers = NULL;
        headers = curl_slist_append(headers, "Content-Type: application/json");

        const char *data = "{\"prompt\": \"hey my name is sonu kumar what do you think about Narendra Modi\", \"model\": \"llama3.2\", \"temperature\": 0.4}";

        curl_easy_setopt(curl, CURLOPT_URL, "https://npmai-api.onrender.com/llm");
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data);

        CURLcode res = curl_easy_perform(curl);
        if(res != CURLE_OK) fprintf(stderr, "Request failed: %s\n", curl_easy_strerror(res));

        curl_easy_cleanup(curl);
        curl_slist_free_all(headers);
    }
    return 0;
}

#Latest Update :
version 0.1.2 Here in this version we added Memory concept so that you do not need to define memory concept and no need to rely on Agentic Frameworks for Memory.

⚠️ Important Notes

Designed for educational ,small-scale experimentation, for demo projets and small scale users.

If using at a larger scale, consider supporting the original AI platforms—they invest heavily in research and infrastructure.

use responsibly to help us.

✅ npmai makes it effortless to connect Ollam models with Python, bringing automation, experimentation, and LangChain,Crew AI integration together in a single, easy-to-use package.