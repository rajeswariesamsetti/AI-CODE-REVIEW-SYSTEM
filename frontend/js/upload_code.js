async function getCodeAndLanguage() {
    let fileInput = document.getElementById("fileInput");
    let codeElement = document.getElementById("code");

    let code = "";
    let language = null;

    if (fileInput.files.length > 0) {
        let file = fileInput.files[0];
        let ext = file.name.split('.').pop().toLowerCase();

        const extMap = {
            'py': 'python',
            'js': 'javascript',
            'c': 'c',
            'cpp': 'cpp',
            'java': 'java'
        };
        language = extMap[ext] || null;

        code = await new Promise((resolve, reject) => {
            let reader = new FileReader();
            reader.onload = e => resolve(e.target.result);
            reader.onerror = e => reject(e);
            reader.readAsText(file);
        });

        // Populate textarea so user sees what was uploaded
        codeElement.value = code;
    } else {
        code = codeElement.value;
        // Basic heuristic for pasted code if no file is uploaded
        if (code.includes('include <iostream>') || code.includes('cout <<')) {
            language = 'cpp';
        } else if (code.includes('include <stdio.h>') || code.includes('printf(')) {
            language = 'c';
        } else if (code.includes('public class ') || code.includes('System.out')) {
            language = 'java';
        } else if (code.includes('console.log') || code.includes('function(') || code.includes('=>')) {
            language = 'javascript';
        } else {
            language = 'python'; // Default assumption for untyped paste
        }
    }

    return { code, language };
}

async function reviewCode() {
    try {
        let { code, language } = await getCodeAndLanguage();

        // Clear stale state specifically because of localhost caching issues.
        localStorage.removeItem("review_report_issues");
        localStorage.removeItem("review_report_score");

        let response = await fetch("http://127.0.0.1:5000/review", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                code: code,
                language: language
            })
        });

        let data = await response.json();

        localStorage.setItem("review_report_issues", JSON.stringify(data.issues || []));

        // Explicit 0 check so we don't accidentally write 'undefined'
        let finalScore = data.score !== undefined ? data.score : 0;
        localStorage.setItem("review_report_score", finalScore);

        window.location.href = "review_report.html";
    } catch (e) {
        alert("Error analyzing code: " + e.message);
    }
}

async function runCode() {
    try {
        let { code, language } = await getCodeAndLanguage();
        let stdin = document.getElementById("stdinInput").value;
        let runOutput = document.getElementById("runOutput");

        runOutput.style.display = "block";
        runOutput.innerText = "Running...\n";

        let response = await fetch("http://127.0.0.1:5000/run", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                code: code,
                language: language,
                stdin: stdin
            })
        });

        let data = await response.json();

        if (data.error) {
            runOutput.innerText = "Error: " + data.error + "\n\n" + (data.stderr || "");
        } else {
            runOutput.innerText = data.stdout + (data.stderr ? ("\nErrors:\n" + data.stderr) : "");
        }

    } catch (e) {
        document.getElementById("runOutput").innerText = "Execution failed: " + e.message;
        document.getElementById("runOutput").style.display = "block";
    }
}