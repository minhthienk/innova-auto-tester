

css = '''
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
  img {
    display: block;
    margin-left: auto;
    margin-right: auto;
  }

  table {
    width:60%;
    margin-left: auto;
    margin-right: auto;
  }
  </style>
</head>

'''

table_screen_show = '''
<table border="0" cellpadding="5" cellspacing="0">
  <tr>
    <th style="font-size:30px">Current Screen</th>
    <th style="font-size:30px">Reference Screen</th>
  </tr>
  <tr>
    <td>
      <img src="data:image/png;base64, {cur}"/>
    </td>
    <td>
      <img src="data:image/png;base64, {ref}"/>
    </td>
  </tr>
</table>
'''

table_text_compare = '''
<table border="1" cellpadding="10" cellspacing="0">
  <tr>
    <th>Text Object</th>
    <th>Current Screen Text</th>
    <th>Reference Screen Text</th>
    <th>Pass/Fail</th>
  </tr>
  {rows}
</table>
'''

row_result = '''
  <tr>
    <td style="text-align:center">
      {obj}
    </td>
    <td>
      {cur}
    </td>
    <td>
      {ref}
    </td>
    <td style="text-align:center">
      {stt}
    </td>
  </tr>
'''

green_line = '''
<table style="background-color:#00FF00" border="0" cellpadding="10" cellspacing="0" height="20px">
  <tr>
  </tr>
</table>
'''

