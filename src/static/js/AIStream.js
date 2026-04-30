async function sendMessage() {
    console.log("点击了发送")
    const inputText = document.getElementById("input_text").value
    const responseDiv = document.getElementById("response")
    responseDiv.innerHTML = ""

    const formData = new FormData
    formData.append(
        "input_text",
        inputText
    )

    const response = await fetch(
        "/chat", 
        {
            method: "POST",
            body: formData
        }
    )
    const reader = response.body.getReader()
    let markdownText = ""

    while (true){
        const {done , value}= await reader.read()
        if (done) {
            break
        }
        const text = new TextDecoder().decode(value)
        markdownText += text
        // 用marked库实时渲染markdown
        responseDiv.innerHTML = marked.parse(markdownText)
    }
}
