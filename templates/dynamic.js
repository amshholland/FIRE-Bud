<script type = "text/javascript">
    var cnt = 0;

    function addForm() {

        var div = document.createElement('DIV');
        div.innerHTML = '<input id="file' + cnt + '" name="file' + '' + '" type="file" />' +
                        '<input id="Button' + cnt + '" type="button" ' + 'value="X" onclick="deleteFile(this)" />';
        document.getElementById("uploadControls").appendChild(div);
        cnt++;
        buttonText();
    }

    function deleteFile(div) {

        document.getElementById("uploadControls").removeChild(div.parentNode);
        cnt--;
        buttonText();
    }

    function buttonText() {

        if (cnt > 0) {
            document.myform.add_button.value = 'Add Another Attachment';
        } else {
            document.myform.add_button.value = 'Add Attachment';
        }
    }
</script>