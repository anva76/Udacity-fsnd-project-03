/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-7un4dhfbx4hxdp18.us', // the auth0 domain prefix
    audience: 'UdacityCoffeeshop', // the audience set for the auth0 app
    clientId: 'zjPbNGE5rZTIVzs9byX5IGQ6OpBrBE5J', // the client id generated for the auth0 app
    callbackURL: 'http://127.0.0.1:8100', // the base url of the running ionic application. 
  }
};
