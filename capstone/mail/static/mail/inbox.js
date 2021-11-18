//var csrftoken = "";
document.addEventListener('DOMContentLoaded', function () {
 // csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#trash').addEventListener('click', () => load_mailbox('trash'));
  document.querySelector('#draft').addEventListener('click', () => load_mailbox('draft'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  var form = document.getElementById("compose-form");
  form.reset()
  form.onsubmit = tosubmit;

}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  var emailsview = document.querySelector('#emails-view');
  emailsview.style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';


  // Show the mailbox name
  emailsview.innerHTML = "";
  emailsview.insertAdjacentHTML("beforeend", "<h3>" + mailbox.charAt(0).toUpperCase() + mailbox.slice(1) + "</h3>");


  Getter("/emails/" + mailbox)
    .then(emails => {
      emails.forEach(email => {
        const link = "emails/" + email.id;
        const bg = email.read === true ? "bg-secondary text-white" : "bg-white";
        console.log(email)
        emailsview.insertAdjacentHTML("beforeend", "<div class='border w-100 p-2 " + bg + "' > <a class='email card-link strong'  read='" + email.read + "'  href=" + link + " > " + email.sender + " </a> <strong> " + email.subject + "</strong>    " + email.timestamp + " </div><br>")
      });

      // ... do something else with email ...
      reademail()
    })
  function reademail() {

    //read emails
    document.querySelectorAll(".email").forEach(function (elm) {

      elm.onclick = (e) => {

        e.preventDefault()
        const ee = e.target;

        if (mailbox === "inbox" && ee.getAttribute("read") === 'false') {
          Postman("PUT", ee.href, { read: true })
        }

        // then get call
        Getter(ee.href).then(email => {
          let link = "emails/" + email.id;
          let recipient = "";
          email.recipients.forEach((s) => recipient += s + ", ");
          var archivemsg = email.archived === true ? "unarchived" : "archived";
          emailsview.innerHTML = "";
          emailsview.innerHTML = "<p class='lead'> <strong>From : </strong> " + email.from_email + " <br><strong>To : </strong>" + recipient + "<br> <strong> Subject : </strong>" + email.subject + "<br> <strong>Timestamp : </strong>" + email.timestamp + "<br><a id='reply' href='#' email='" + email.sender + "' subject='"+email.subject+"' >Reply</a>  |  <a id='archive' archived=" + email.archived + " href=" + link + "  > " + archivemsg + "</a> <hr><br> " + email.body + "</p>"
          // read and archive
          sortout();
        });

      }
    })

  }

}
function sortout() {
  // sortout replies
  document.getElementById("reply").onclick = function (re) {
    re.preventDefault()
    compose_email()
    document.querySelector("#compose-recipients").value = re.target.getAttribute("email");
    document.querySelector("#compose-subject").value = "Re: "+ re.target.getAttribute("subject");
  }


  // sortout archive
  document.getElementById("archive").onclick = function (e) { 
    e.preventDefault() 
 
    let ee = e.target;
    let arrv = ee.getAttribute("archived") === 'true' ? false:true

    Postman("PUT", ee.href, {
      archived: arrv
    }).then(archiveResponse => {
      load_mailbox('inbox')
    });
  }
}

function tosubmit(e) {
  e.preventDefault()
  var form = e.target;
  if (form.checkValidity() === false) {

    return false;
  }

  let elms = form.elements;

  const options = {
    recipients: elms.namedItem('compose-recipients').value,
    subject: elms.namedItem('compose-subject').value,
    body: elms.namedItem('compose-body').value,
  }

  Postman("POST", "/emails", options).then(response => {
    console.log(response);
    load_mailbox('sent')
  });
};

async function Getter(url) {
  return fetch(url)
    .then(response => response.json())
}

async function Postman(method, url, bodyarg) {

  const options = {
    method: method,
    mode: 'same-origin', // Do not send CSRF token to another domain.,
    body: JSON.stringify(bodyarg)
  }
  const request = new Request(
    url,
    //{ headers: { 'X-CSRFToken': csrftoken } }
  );
  if (method === "PUT")
    return fetch(request, options)
  return fetch(request, options)
    .then(response => response.json())
}