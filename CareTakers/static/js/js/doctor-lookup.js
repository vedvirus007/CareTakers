// var apiKey = require('./../.env').apiKey;

// function Doctor(medicalIssue) {
//   this.medicalIssue = medicalIssue;
// }

// Doctor.prototype.getDoctors = function(medicalIssue,row, displayDocName, displayTitle, displaySpeciality, displayPracticeName,displayaddress) {
//   $.get('https://api.betterdoctor.com/2016-03-01/doctors?query='+ medicalIssue+'&location=45.5231%2C-122.6765%2C%205&user_location=45.5231%2C-122.6765&skip=0&limit=20&user_key=' + apiKey)
//   .then(function(result) {
//     (result.data.forEach(function(data) {
//       row();
//       var docName = data.profile.first_name + " " + data.profile.last_name;
//       displayDocName(docName);
//       displayTitle(data.profile.title);
//       displaySpeciality(data.specialties[0].description);
//       displayPracticeName(data.practices[0].name);
//       var practiceAddress = data.practices[0].visit_address.street + " " + data.practices[0].visit_address.street2 + " " +  data.practices[0].visit_address.zip;
//       displayaddress(practiceAddress);
//       console.log(result);
//     }));
//   })
//   .fail(function(error){
//     $('.showDoctors').text(error.responseJSON.message);
//     });
//   };

//   exports.doctorModule = Doctor;
