
var file_input = document.getElementById('file_input');
var preview = document.getElementById('avatar_preview');
    console.log(file_input);
    console.log(preview);

file_input.addEventListener('change',function(){
    if(!file_input.value){
        return ;
    }

    var file = file_input.files[0];
    if(file.type != 'image/jpeg' && file.type != 'image/png'){
        alert('不是有效的文件类型！');
        return ;
    }

    var reader = new FileReader();
    reader.onload = function(e){
        var 
            data = e.target.result;
        preview.src = data;
    };
    reader.readAsDataURL(file);
})