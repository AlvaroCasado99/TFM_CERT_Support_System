""" Aquí se guardan patrones usados en la aplicaión """

malicious_html_patterns = [
        r'<script.*?>.*?</script>',  
        r'<iframe.*?>.*?</iframe>',  
        r'javascript:',             
        r'on\w+\s*=',              
        r'<object.*?>.*?</object>', 
        r'<embed.*?>.*?</embed>'
    ]
