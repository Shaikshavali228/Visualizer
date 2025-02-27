document.getElementById("run").addEventListener("click", async function() {
    let code = document.getElementById("code").value;
    let language = document.getElementById("language").value;
    
    const response = await fetch("/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code: code, language: language })
    });

    const result = await response.json();
    document.getElementById("output").innerText = result.output;
    
    visualizeExecution(code);
});

function visualizeExecution(code) {
    let lines = code.split("\n");
    let executionDiv = document.getElementById("execution");
    executionDiv.innerHTML = "";

    let index = 0;
    function highlightLine() {
        if (index >= lines.length) return;
        
        executionDiv.innerHTML = "";
        for (let i = 0; i < lines.length; i++) {
            let lineText = document.createElement("div");
            lineText.textContent = lines[i];
            if (i === index) {
                lineText.innerHTML = `➡️ <span class="arrow">${lines[i]}</span>`;
            }
            executionDiv.appendChild(lineText);
        }
        index++;
        setTimeout(highlightLine, 1000);
    }
    
    highlightLine();
}
