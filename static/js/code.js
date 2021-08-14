        // form

        $(document).ready(
            function(){
                $('.main_form').hide()
            }
        )

        $(document).ready(
            function(){
                $('.add-password').click(
                    function(){
                        $('.main_form').show()
                        $(this).hide()
                    }
                )
            }
        )

        $(document).ready(
            function(){
                $('.cancel-form').click(
                    function(){
                        $('.main_form').hide()
                        $('.add-password').show()
                    }
                )
            }
        )

navButton = () =>{
    let button = document.getElementById('toggle-button').className
    if(button == 'fas fa-angle-down'){
        document.getElementById('toggle-button').className = 'fas fa-angle-up'
    }else{
        document.getElementById('toggle-button').className = 'fas fa-angle-down'
    }

}