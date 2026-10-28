
const form = document.getElementById("uploadForm");
const fileInput = document.getElementById("document");
const button = document.getElementById("analyzeButton");
const message = document.getElementById("message");
const results = document.getElementById("results");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const file = fileInput.files[0];

    if (!file) {
        message.textContent = "Please select a document first.";
        return;
    }

    const allowedExtensions = [".pdf", ".docx"];
    const extension = file.name
        .substring(file.name.lastIndexOf("."))
        .toLowerCase();

    if (!allowedExtensions.includes(extension)) {
        message.textContent = "Please upload a PDF or DOCX file.";
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    button.disabled = true;
    message.textContent = "Analyzing document...";
    results.hidden = true;

    try {
        const response = await fetch("/analyze", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Document analysis failed.");
        }

        // 1. Display document summary
        document.getElementById("summary").textContent = data.summary;

        // 2. Display extracted entities
        const entitiesDiv = document.getElementById("entities");
        entitiesDiv.replaceChildren();

        for (const [key, value] of Object.entries(data.entities)) {
            const paragraph = document.createElement("p");
            const label = document.createElement("strong");

            label.textContent = key.replaceAll("_", " ") + ": ";
            paragraph.append(
                label,
                document.createTextNode(value ?? "Not found")
            );

            entitiesDiv.appendChild(paragraph);
        }

        // 3. Display validation status
        const validation = data.validation;
        const status = document.getElementById("validationStatus");

        status.textContent = validation.is_valid
            ? "Validation passed"
            : "Validation failed";

        status.style.color = validation.is_valid ? "green" : "red";

        // 4. Display validation errors
        const errorsList = document.getElementById("errors");
        errorsList.replaceChildren();

        (validation.errors || []).forEach((error) => {
            const item = document.createElement("li");
            item.textContent = error;
            errorsList.appendChild(item);
        });

        // 5. Display validation warnings
        const warningsList = document.getElementById("warnings");
        warningsList.replaceChildren();

        (validation.warnings || []).forEach((warning) => {
            const item = document.createElement("li");
            item.textContent = warning;
            warningsList.appendChild(item);
        });

        // 6. Display human review result
        const humanReview = data.human_review;
        let reviewSection = document.getElementById("humanReview");

        // Create the section if it does not already exist in HTML
        if (!reviewSection) {
            reviewSection = document.createElement("section");
            reviewSection.id = "humanReview";
            results.appendChild(reviewSection);
        }

        reviewSection.replaceChildren();

        const reviewHeading = document.createElement("h3");
        reviewHeading.textContent = "Human Review";
        reviewSection.appendChild(reviewHeading);

        const reviewStatus = document.createElement("p");

        if (humanReview?.required) {
            reviewStatus.textContent =
                "Review required: Please check the flagged information.";
            reviewStatus.style.color = "red";
        } else {
            reviewStatus.textContent =
                "No human review flagged by the current checks.";
            reviewStatus.style.color = "green";
        }

        reviewSection.appendChild(reviewStatus);

        const reviewFields = document.createElement("p");
        reviewFields.textContent =
            "Fields requiring review: " +
            (
                humanReview?.fields?.length
                    ? humanReview.fields.join(", ")
                    : "None"
            );

        reviewSection.appendChild(reviewFields);

        // 7. Display prototype confidence indicators
        const prototype = data.prototype_result;

        let prototypeSection =
            document.getElementById("prototypeResults");

        if (!prototypeSection) {
            prototypeSection = document.createElement("section");
            prototypeSection.id = "prototypeResults";
            results.appendChild(prototypeSection);
        }

        prototypeSection.replaceChildren();

        const prototypeHeading = document.createElement("h3");
        prototypeHeading.textContent = "Prototype Processing Results";
        prototypeSection.appendChild(prototypeHeading);

        const confidence = prototype?.confidence || {};

        for (const [field, score] of Object.entries(confidence)) {
            const paragraph = document.createElement("p");
            paragraph.textContent =
                field.replaceAll("_", " ") +
                ": " +
                Math.round(score * 100) +
                "% pattern-match indicator";

            prototypeSection.appendChild(paragraph);
        }

        // 8. Display extracted text
        document.getElementById("extractedText").textContent =
            data.extracted_text;

        results.hidden = false;
        message.textContent = "Document analyzed successfully.";

    } catch (error) {
        message.textContent = "Error: " + error.message;
    } finally {
        button.disabled = false;
    }
});
