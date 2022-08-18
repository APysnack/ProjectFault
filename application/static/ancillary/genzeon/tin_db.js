const addTINBtn = document.querySelector("#addTINBtn");
const addTINForm = document.querySelector(".addTINForm");
const addTINInput = document.querySelector("#addTINInput");
const addSubmit = document.querySelector("#addSubmit");
const addDocBtn = document.querySelector("#addDocBtn");
const addDocForm = document.querySelector(".addDocForm");
const addDocInput = document.querySelector("#addDocInput");
const docSubmit = document.querySelector("#docSubmit");
const searchTINBtn = document.querySelector("#searchTINBtn");
const tinListContainer = document.querySelector(".tinListContainer");
const searchTINInput = document.querySelector("#searchTINInput");
const searchContainer = document.querySelector(".searchContainer");
const dataColsBtn = document.querySelector("#addDataCol");
const headerColsBtn = document.querySelector("#addHeaderCol");
const delHeaderCol = document.querySelector("#delHeaderCol");
const delDataCol = document.querySelector("#delDataCol");
const downloadDBBtn = document.querySelector("#downloadDBBtn");

const sharePointLink = document.querySelector("#sharePointLink");
const devOpsLink = document.querySelector("#devOpsLink");
const tinSelector = document.querySelector("#tinSelector");
const modelSelector = document.querySelector("#modelSelector");

currentDisplay = 'search'
var newTIN = {}
var newDoc = {}
var parentElement = null

var colsArray = ['Description', 'Other Codes (HCPCS/CPT)', 'Procedure Code', 'Rev Code', 'Svc Code', 'Svc Date', 'Quantity', 'Total Chgs', 'Unit Price']

docSubmit.addEventListener('click', (e)=>{
    if(addDocInput.value && sharePointLink.value && devOpsLink.value && tinSelector.value){
        newDoc.title = addDocInput.value
        newDoc.sharepoint = sharePointLink.value
        newDoc.devops = devOpsLink.value
        newDoc.tin = tinSelector.value
        let headerArray = []
        let dataArray = []
        
        const headers = document.querySelectorAll('.headColField')
        const data = document.querySelectorAll('.dataColField')

        for(let i = 0; i < headers.length; i++){
            headerArray.push(headers[i].value)
        }
        for(let i = 0; i < data.length; i++){
            dataArray.push(data[i].value)
        }

        newDoc.headers = headerArray
        newDoc.data = dataArray

        submitDocument(newDoc)
    }
    else{
        e.preventDefault()
        alert('Form is missing data')
    }
})

downloadDBBtn.addEventListener('click', (e)=>{
    pullDB()
})

delHeaderCol.addEventListener('click', (e)=>{
    removeSelector('head')
})

delDataCol.addEventListener('click', (e)=>{
    removeSelector('data')
})

headerColsBtn.addEventListener('click', (e)=>{
    addSelector('head')
})

dataColsBtn.addEventListener('click', (e)=>{
    addSelector('data')
})

function addSelector(type){
    var select = document.createElement("select");
    for(let i = 0; i < colsArray.length; i++){
        select.options.add( new Option(colsArray[i]));
    }
    select.style.margin = '1% 2% 0 0';
    if(type == 'head'){
        parentElement = document.getElementById("headerColContainer");
        select.classList.add("headColField")
    }
    else{
        parentElement = document.getElementById("dataColContainer");
        select.classList.add("dataColField")
    }
    parentElement.appendChild(select);
}

function removeSelector(type){
    if(type == 'head'){
        parentElement = document.getElementById("headerColContainer");
    }
    else{
        parentElement = document.getElementById("dataColContainer");
    }
    if(parentElement.lastElementChild){
        parentElement.removeChild(parentElement.lastElementChild);
    }
}

addTINBtn.addEventListener('click', (e)=>{
    if(currentDisplay != 'add'){
        currentDisplay = 'add'
        updateDisplay()
    }
});

addDocBtn.addEventListener('click', (e)=>{
    if(currentDisplay != 'addDoc'){
        currentDisplay = 'addDoc'
        updateDisplay()
    }
});

searchTINBtn.addEventListener('click', (e)=>{
    if(currentDisplay != 'search'){
        currentDisplay = 'search'
        updateDisplay()
    }
});

addSubmit.addEventListener('click', (e)=>{
    if(addTINInput.value){
        newTIN.num = addTINInput.value
        newTIN.model = modelSelector.value
        console.log(newTIN)
        callAjax(newTIN)
    }
})

function updateDisplay(){
    if(currentDisplay == 'search'){
        addTINForm.style.display = 'none';
        addDocForm.style.display = 'none';
        searchContainer.style.display = 'flex';
        tinListContainer.style.display = 'flex';
    }
    else if(currentDisplay == 'addDoc'){
        addTINForm.style.display = 'none';
        addDocForm.style.display = 'flex';
        searchContainer.style.display = 'none';
        tinListContainer.style.display = 'none';
    }
    else{
        addTINForm.style.display = 'flex';
        addDocForm.style.display = 'none';
        searchContainer.style.display = 'none';
        tinListContainer.style.display = 'none';
    }
}

function searchList(){
    var input, filter, ul, li, a, i, txtValue;
    filter = searchTINInput.value.toLowerCase();
    // ul --> tinListContainer
    li = tinListContainer.getElementsByTagName('li');
    for (let i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName("a")[0];
        txtValue = a.textContent || a.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          li[i].style.display = "";
        } else {
          li[i].style.display = "none";
        }
    }
}

function compileDB(data){
    const rows = [['ID', 'TIN ID', 'Doc Title', 'Header Columns', 'Data Columns', 'Storage Link', 'Bugs Link', 'Model Type']]
    var tempArray = []
    var dataCols = ''
    var headerCols = ''
    var comments = ''

    for(let i = 0; i < data.length; i++){
        tempArray = []
        tempArray.push(data[i].id)
        tempArray.push(data[i].tin_id)
        tempArray.push(data[i].name)
        headerCols = ''
        for(let k = 0; k < data[i].header_cols.length; k++){
            headerCols += data[i].header_cols[k]
            headerCols += '; '
        }
        tempArray.push(headerCols)
        dataCols = ''
        for(let k = 0; k < data[i].data_cols.length; k++){
            dataCols += data[i].data_cols[k]
            dataCols += '; '
        }
        tempArray.push(dataCols)
        rows.push(tempArray)
        tempArray.push(data[i].storage_url)
        tempArray.push(data[i].bugs_url)
        tempArray.push(data[i].model_type)
        tempArray.push(comments)
    }
  
    let csvContent = "data:text/csv;charset=utf-8,";
    
    rows.forEach(function(rowArray) {
        let row = rowArray.join(",");
        csvContent += row + "\r\n";
    });
    var encodedUri = encodeURI(csvContent);
    var encodedUri = encodeURI(csvContent);
    var link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "tin_db.csv");
    document.body.appendChild(link);
    link.click(); 
}


function callAjax(newTIN){
    jQuery.ajax({ 
         url: "/api/add_tin",
         type: 'POST', 
         contentType: 'application/json',
         data: JSON.stringify(newTIN),
         dataType: 'json',
         timeout: 5000,
         success: function(response) { 
              location.reload();
       }
    })
}

function submitDocument(newDoc){
    jQuery.ajax({ 
         url: "/api/add_doc",
         type: 'POST', 
         contentType: 'application/json',
         data: JSON.stringify(newDoc),
         dataType: 'json',
         timeout: 5000,
         success: function(response) { 
              location.reload();
       }
    })
}

function pullDB(){
    jQuery.ajax({ 
         url: "/api/get-doc-db",
         type: 'GET', 
         timeout: 5000,
         success: function(data) { 
            if (data) {
              compileDB(data)
            }
       }
    })
}

document.onload = updateDisplay()