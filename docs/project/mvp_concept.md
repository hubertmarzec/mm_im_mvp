# Application – Email Classification (MVP)

### Main Problem
A law firm has accumulated a massive number of historical emails with attachments (documents, contracts, legal letter templates). Manually searching through and categorizing these messages is extremely time-consuming and inefficient, making it difficult to quickly find specific types of documents in the mailbox.

### Minimal Set of Functionalities
- **Authentication** (user login)
- **Ability to upload a single email** in EML format along with its attachments
- **Metadata extraction** from the email (sender, recipient, date, subject, list of attachments)
- **Classification of each attachment** by an LLM into one of several categories (e.g., contract, legal brief, etc.)
- **Saving the data in the system**: a record representing the email and records of its attachments with classification results
- **Viewing the list of emails** along with their attachments
- **Filtering** by the sender of the email or the type of attachment
- **Option to download** the attachment

### What Is NOT Included in the MVP
- **User account management** (e.g., role creation, password reset, profile editing)
- **Importing any format other than EML**
- **Mobile application**

### Success Criteria
- **90%** of emails (or attachments, to be clarified) are correctly classified.