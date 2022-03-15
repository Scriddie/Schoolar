// var p_array = Array.from(profile_list);
// typeof profile_list;
// show_suggestions();

# seems to work only with single element in list
var profile_list = {{ list | safe }};

// add links dynamically
// var profile_list = {{ list | tojson | safe }};
// var profile_list = JSON.parse('{{ profile_list | safe }}');
// for (var p in profile_list) {
//     console.log(p, profile_list[p]);
//     option = document.createElement('a');
//     option.innerHTML = "{{profile_list[p]}}";
//     dropdown.appendChild(option);
// }
