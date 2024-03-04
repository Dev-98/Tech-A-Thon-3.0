document.getElementById('analyzeButton').addEventListener('click', function() {
    var fileInput = document.getElementById('resumeInput');
    var analysisResults = document.getElementById('analysisResults');
  
    if (fileInput.files.length > 0) {
      var file = fileInput.files[0];
      var reader = new FileReader();
  
      reader.onload = function(event) {
        var text = event.target.result;
        // Here you can perform text analysis on 'text'
        // For simplicity, let's just display the text for now
        analysisResults.innerText = text;
      };
  
      reader.readAsText(file);
    } else {
      analysisResults.innerText = "Please select a file.";
    }
  });
  