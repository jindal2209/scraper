document.getElementById('select_all').onchange = function() {
  var checkboxes = document.getElementsByName('value_checkbox');
  for (var checkbox of checkboxes) {
      checkbox.checked = this.checked;
      }
  }