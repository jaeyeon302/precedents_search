
var updateDownloadProgressID = null;
//replaceAll prototype 선언
String.prototype.replaceAll = function(org, dest) {
    return str.replace(/#/gi, ""); 
}

function Precedent(precedentID,precedentText,idx=-1){
    let splitted = precedentText.split('\n');
    this.idx = idx;
    this.text = precedentText;
    this.precedentID = precedentID;
    this.pansi = ""
    this.yozi = ""
    this.jomun = ""
    this.all = ""
    this.reference = ""
    this.succeess = false;

    for(let i = 0 ; i<splitted.length-1; i++){
        let line = splitted[i];
        let nextLine = splitted[i+1].trim();
        nextLine = nextLine.replace(/】\n/gi, "】"); 
        nextLine = nextLine.replace(/【/gi, "\n【");
        nextLine = nextLine.replace(/\t/gi, ""); 
        nextLine = nextLine.replace(/  /gi, ""); 

        if(line.includes('【판시사항】')){
            this.succeess = true;
            this.pansi = nextLine;
        }else if(line.includes('【판결요지】')){
            this.succeess = true;
            this.yozi = nextLine;
        }else if(line.includes('【참조조문】')){
            this.succeess = true;
            this.jomun = nextLine;
        }else if(line.includes('【참조판례】')){
            this.succeess = true;
            this.reference = nextLine;
        }else if(line.includes('【전문】' )){
            this.succeess = true;
            let allLines = nextLine;
            for(let j=i+2;j<splitted.length;j++){
                allLines = allLines + splitted[j];
            }
            allLines = allLines.replace(/】\n/gi, "】"); 
            allLines = allLines.replace(/【/gi, "\n【"); 
            allLines = allLines.replace(/\t/gi, ""); 
            allLines = allLines.replace(/  /gi, ""); 
            this.all = allLines;
        }
    }
    this.makeSlide = ()=>{
        if(this.succeess){
            return '<div class="slide">'+
                        '<div class="title">' + this.precedentID + '</div>'+
                        '<div class="subtitle">' + "판시사항" + '</div>'+
                        '<div class="content">' + this.pansi + '</div>'+
                        '<div class="subtitle">' + "판결요지" + '</div>'+
                        '<div class="content">' + this.yozi + '</div>'+
                        '<div class="subtitle">' + "참조판례" + '</div>'+
                        '<div class="content">' + this.reference + '</div>'+
                        '<div class="subtitle">' + "전문" + '</div>'+
                        '<pre class="content">' + this.all + '</pre>'+
                    '</div>';
        }else{
            return '<div class="slide error-slide">'+
                        '<div class="title">' + this.precedentID + '</div>'+
                        '<div class="error">' + "잘못된 판례번호! 이거나" + '</div>'+
                        '<div>' + "국가법령정보 한글 판례 검색에서 못 찾았을 수 있습니다."+"</div>"+
                        
                    '</div>';
        }
    }

}
function getPrecedents(numbers){
    let cases = [];
    let progressCount = 0;
    let baseURL = "https://www.law.go.kr/"
    let url = ""
    let domParser = new DOMParser();
    let doc = null;

    updateDownloadProgressID = setInterval(()=>{
        $("#percent").text( 100*(progressCount+1)/numbers.length + "%");
    },100);

    for(let i = 0; i<numbers.length;i++){
        url = baseURL + "/판례/("+numbers[i]+")";
        fetch(url).then(r=>r.text()).then(
            result=>{
                doc = domParser.parseFromString(result,'text/html');
                let src = baseURL + $(doc).find('iframe').attr('src');
                fetch(src).then(r=>r.text()).then(
                    result=>{
                        let content=domParser.parseFromString(result,'text/html');
                        content = $(content).find('.pgroup')[0].innerText;
                        cases.push(new Precedent(numbers[i], content, i));
                        progressCount += 1;
                    }
                ).catch(err=>{
                    console.log(err);
                    let precedent = new Precedent(numbers[i],"",i);
                    cases.push(precedent);
                })
            }
        ).catch(err=>{
            console.log(err);
            let precedent = new Precedent(numbers[i],"",i);
            cases.push(precedent);
        })
    }
    return cases;
}


function addOnLoad(fn){ 
    var old = window.onload;
    window.onload = function()
    {
        if(old){
            old();
        }
        fn();
    };
 }


$(document).ready(function(){
    let newDataLoaded = false;
    var precedents = null;

        
    $('#submit').click(function(){
        
        precedents = null;
        let numbers = $('.numbers').val();
        numbers = numbers.trim();
        if(numbers.includes(',')){
            numbers = numbers.split(',');
        }else if(numbers.includes(' ')){
            numbers = numbers.split(' ')
        }else{
            numbers = [numbers]
        }
        numbers = numbers.map(i=>i.trim());
        precedents = getPrecedents(numbers);
        let slideContainer = $('.slide-container');
        let timerId = setInterval( ()=>{
            console.log("hi");
            if(precedents.length==numbers.length) {
                let fails = precedents.filter((it)=>!it.succeess)
                $("#num-of-fail").text(fails.length+"/"+precedents.length);
                $("#fail-cases").text(fails.map(it=>it.precedentID).toString());

                clearInterval(timerId);
                clearInterval(updateDownloadProgressID);

                console.log(precedents);
                newDataLoaded = true
                slideContainer.empty();

                precedents.sort((a,b)=>{
                    if(a.idx > b.idx){
                        return 1;
                    }else if(a.idx < b.idx){
                        return -1;
                    }else{
                        return 0;
                    }
                });

                precedents.map(it=>{
                    slideContainer.append(it.makeSlide());
                });                
            }
        },100);
    });

    $("#save").click(function(){
        console.log("저장!")
        if(precedents!=null){
            console.log("??")
            //var element = document.getElementsByClassName('slide-container');
            let failures = precedents.filter((it)=>!it.succeess)
            failures = failures.map(it=>it.precedentID)
            failures = failures.map(it=> new docx.Paragraph({
                text: "\n"+it+"\n"
            }))
            failures.unshift(
                new docx.Paragraph({
                    text:"\n실패 케이스\n",
                    bold:true
                })
            )

            const doc = new docx.Document();

            doc.addSection({
                properties:{},
                children:failures
            })

            let saveOption = $("input:checkbox[name=save]").filter((it,elem)=>elem.checked)
                                                           .map((it,elem)=>elem.value)
            saveOption = saveOption.toArray();

            for(let i = 0; i<precedents.length;i++){
                let element = precedents[i];
                if(element.succeess){
                    let children = [];
                    children.push(
                        new docx.Paragraph({
                            text:"\n"+element.precedentID+"\n",
                            heading:docx.HeadingLevel.HEADING_1,
                            bold:true,
                            color:"000000", 

                        })
                    )
                    if(saveOption.includes("pansi")){
                        children.push( 
                            new docx.Paragraph({
                                text:"\n판시사항\n",
                                heading: docx.HeadingLevel.HEADING_2,
                                bold:true
                            })
                        )
                        children.push(
                            new docx.Paragraph({
                                children:[
                                    new docx.TextRun("\n"+element.pansi)
                                ]
                            })
                        )
                    }
                    if(saveOption.includes("yozi")){
                        children.push( 
                            new docx.Paragraph({
                                text:"\n판결요지\n",
                                heading: docx.HeadingLevel.HEADING_2,
                                bold:true
                            })
                        )
                        children.push(
                            new docx.Paragraph({
                                children:[
                                    new docx.TextRun("\n"+element.yozi)
                                ]
                            })
                        )
                    }
                    if(saveOption.includes("reference")){
                        children.push(new docx.Paragraph({
                            text:"\n참조판례\n",
                            heading: docx.HeadingLevel.HEADING_2,
                            bold:true
                        }))
                        children.push(new docx.Paragraph({
                            children:[
                                new docx.TextRun("\n"+element.reference)
                            ]
                        }))
                    }
                    if(saveOption.includes("all")){
                        children.push(new docx.Paragraph({
                            text:"\n전문\n",
                            heading: docx.HeadingLevel.HEADING_2,
                            bold:true
                        }))
                        children.push(new docx.Paragraph({
                            children:[
                                new docx.TextRun("\n"+element.all+"\n")
                            ]
                        }))
                    }

                    doc.addSection({
                        properties:{},
                        headers:{
                            default: new docx.Header({
                                children:[new docx.Paragraph(element.precedentID)]
                            })
                        },
                        children:children
                    })
                }

            }
               
            docx.Packer.toBlob(doc).then(blob=>{
                console.log(blob);
                let name = ""
                if(saveOption.includes("pansi")) name += "_판시사항";
                if(saveOption.includes("yozi")) name += "_판결요지";
                if(saveOption.includes("reference")) name += "_참조판례";
                if(saveOption.includes("all")) name += "_전문";
                name = "판례"+name+".docx"
                saveAs(blob,name);
            })

        }else{
            alert("저장할 것이 없음!");
        }
    })
})

