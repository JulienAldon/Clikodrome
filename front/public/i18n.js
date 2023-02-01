import i18n from "i18next";
import { initReactI18next } from "react-i18next";

// the translations
// (tip move them in a JSON file and import them,
// or even better, manage them separated from your code: https://react.i18next.com/guides/multiple-translation-files)
const resources = {
  en: {
    translation: {
        'Create session' : 'Create session',
        'Create morning session' : 'Create morning session',
        'Morning': 'Morning',
        'Error': 'Error',
        'No clikodrome session can be created today : no edusign session available.': 'No clikodrome session can be created today : no edusign session available.',
        'Information' : 'Information',
        'Morning clicodrome session created.': 'Morning clicodrome session created.',
        'Create evening session': 'Create evening session',
        'Evening': 'Evening',
        'Session already created for this date and hour': 'Session already created for this date and hour',
        'Evening clicodrome session created.': 'Evening clicodrome session created.',
        'Delete the session': 'Delete the session',
        'Session deleted successfully.': 'Session deleted successfully.',
        'Students status has been saved.' : 'Students status has been saved.',
        'Allow session to be signed.': 'Allow session to be signed.',
        'Session has been validated.' : 'Session has been validated',
        'Send all emails for the session.': 'Send all emails for the session.',
        'Send emails': 'Send emails',
        'Session need validation by clicking on Validate.': 'Session need validation by clicking on Validate.',
        'All emails have been sent.': 'All emails have been sent.',
        'Destroy and recreate session, fetching all students an other time.': 'Destroy and recreate session, fetching all students an other time.',
        'Refresh Session': 'Refresh Session',
        'Session could not be refreshed': 'Session could not be refreshed',
        'Session correctly refreshed.': 'Session correctly refreshed.',
        'Search Student': 'Search Student',
        'Login': 'Login',
        'Present': 'Present',
        'Late': 'Late',
        'Validate': 'Validate',
        'All sessions': 'All sessions',
        'Remote period added for': 'Remote period added for :',
        'Please fill out all input.': 'Please fill out all input.',
        'Select student': 'Select student',
        'Date of the start of remote.': 'Date of the start of remote.',
        'Begin': 'Begin',
        'End': 'End',
        'Add': 'Add',
        'Add a new remote student.': 'Add a new remote student.',
        'Remote Students': 'Remote Students',
        'Start date': 'Start date',
        'End date': 'End date',
        'Remote': 'Remote',
        'Remove': 'Supprimer',
        'Remote period removed for': 'Remote period removed for',
        'Cohesive Listing Initiative Concerning Official Date Recollection Over Mediocre Edusign': 'Cohesive Listing Initiative Concerning Official Date Recollection Over Mediocre Edusign',
        'Why clicodrome ?': 'Why clicodrome ?',
        'How to use the clicodrome ?': 'How to use the clicodrome ?',
        'What clicodrome do ?': 'What clicodrome do ?',
        'What clicodrome doesn\'t do ?': 'What clicodrome doesn\'t do ?',
        'Set early departure in edusign (feel free to make a PR with the functionnality).': 'Set early departure in edusign (feel free to make a PR with the functionnality).',
        'Justified absences are not supported, you still need to upload manually for each edusign session. (this might be a future feature)': 'Justified absences are not supported, you still need to upload manually for each edusign session. (this might be a future feature)',
        'Login with office 365': 'Login with office 365',
        'Sessions': 'Sessions',
        'Logout': 'Logout',
    }
  },
  fr: {
    translation: {
        'Create session' : 'Créer session',
        'Create morning session' : 'Créer la session du matin',
        'Morning': 'Matin',
        'Error': 'Erreur',
        'No clikodrome session can be created today : no edusign session available.': 'Les session clikodromes ne peuvent pas être créées aujourd\'hui : pas de session edusign existante.',
        'Information' : 'Information',
        'Morning clicodrome session created.' : 'La session clicodrome du matin à été créée.',
        'Create evening session': 'Créer la session du soir',
        'Evening': 'Soir',
        'Session already created for this date and hour': 'La session à déja été créée pour cette date et heure.',
        'Evening clicodrome session created.': 'La session clicodrome du soir à été créée',
        'Delete the session': 'Supprimer la session',
        'Session deleted successfully.': 'La session à bien été supprimée.',
        'Students status has been saved.' : 'Le statut de l\'élève à été mis à jour.',
        'Allow session to be signed.': 'Autorise les sessions à être signés',
        'Session has been validated.': 'La session à été validée',
        'Send all emails for the session.': 'Envoi tous les mails pour la session.',
        'Send emails': 'Envoi emails',
        'Session need validation by clicking on Validate.': 'La session doit d\'abord être validée avec le bouton Valider.',
        'All emails have been sent.': 'Tous les emails ont été envoyés.',
        'Destroy and recreate session, fetching all students an other time.': 'Met à jour la session avec les informations actuelles de l\'intranet',
        'Refresh Session': 'Actualiser la Session',
        'Session could not be refreshed': 'La session n\'a pas pu être actualisée.',
        'Session correctly refreshed.': 'La session à été actualisée avec succes.',
        'Search Student': 'Chercher un élève',
        'Login': 'Identifiant',
        'Present': 'Présent',
        'Late': 'Retard',
        'Validate': 'Valider',
        'All sessions': 'Toutes les sessions',
        'Remote period added for': 'Periode de télétravail autorisé pour :',
        'Please fill out all input.': 'Vous devez remplir toute les entrés',
        'Select student': 'Selectionner un élève.',
        'Date of the start of remote.': 'Date de début de télétravail.',
        'Begin': 'Début',
        'End': 'Fin',
        'Add': 'Ajouter',
        'Add a new remote student.': 'Ajouter un nouvel élève en télétravail',
        'Remote Students': 'Élève en télétravail',
        'Start date': 'Date de début',
        'End date': 'Date de fin',
        'Remove': 'Supprimer',
        'Remote period removed for': 'Periode télétravail supprimée pour',
        'Cohesive Listing Initiative Concerning Official Date Recollection Over Mediocre Edusign': 'Cohesive Listing Initiative Concerning Official Date Recollection Over Mediocre Edusign',
        'Why clicodrome ?': 'Pourquoi clicodrome ?',
        'How to use the clicodrome ?': 'Comment utiliser clicodrome ?',
        'What clicodrome do ?': 'Que fait clicodrome ?',
        'What clicodrome doesn\'t do ?': 'Que ne fait pas clicodrome ?',
        'Set early departure in edusign (feel free to make a PR with the functionnality).': 'Definir le départ anticipé pour un élève.',
        'Justified absences are not supported, you still need to upload manually for each edusign session. (this might be a future feature)': 'Les absences justifiés doivent être déclarés sur la plateforme edusign directement.',
        'Login with office 365': 'Se connecter avec office 365',
        'Sessions': 'Sessions',
        'Remote': 'Télétravail',
        'Logout': 'Se déconnecter'
      }
  }
};

i18n
.use(initReactI18next) // passes i18n down to react-i18next
.init({
resources,
lng: "en", // language to use, more information here: https://www.i18next.com/overview/configuration-options#languages-namespaces-resources
// you can use the i18n.changeLanguage function to change the language manually: https://www.i18next.com/overview/api#changelanguage
// if you're using a language detector, do not define the lng option

interpolation: {
    escapeValue: false // react already safes from xss
}
});

export default i18n;