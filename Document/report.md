# Record Management System | Project Report

This report explains the thought process, planning, and decisions that went into building the Record Management System for the ICT Department of the *{confidential}*. It covers how the initial idea was formed, the challenges identified during early discussions and how those challenges shaped the final system design. The goal is to show the reasoning behind each feature and how the solution evolved to meet real departmental needs.

### Problem Analysis and Solution Development

While planning the **Record Management System** for the ICT Department of the *{confidential}*, a few practical issues quickly came up. At first, the idea was to let users from different departments log their complaints directly through the system. But this raised several concerns about authenticity, access control and data security.

The project was prompted by the way **repair records were being managed manually**, using pen and paper. This method was not only inefficient but also prone to errors, los, and delays. In a modern world and especially within an ICT department such a process shouldn’t still rely on manual entries. The aim was to digitize and streamline this process, making it more secure, structured and reliable.

#### Problem Identification

Some of the main issues identified were:

- **Impersonation risk:** Anyone could pretend to be from a department and log a complaint.
    
- **No proper confirmation process:** There was no sure way to confirm that the department actually reviewed and approved the repair work.
    
- **Unclear access levels:** It wasn’t clear who should have access to view or manage the records. Allowing open access could expose sensitive internal ICT information.
    
- **Risk of tampering:** There was nothing to stop someone from changing a department’s feedback after submission (like switching “non-satisfactory” to “satisfactory”).
    

#### System Planning and Design Review

To address these problems, I came up with several ideas:

- Letting other departments submit complaints freely was dropped because it made impersonation too easy.
    
- Giving every department access to ICT logs didn’t seem right either as it could lead to data leaks.
    
- Keeping the confirmation part on paper wasn’t ideal since handwritten forms could get lost or altered.
    

During this stage, another idea came up: **the Head of Hardware should have control over creating and managing ICT personnel accounts**. For each new ICT staff member, the system sets their **surname as the default password**, which they can change after their first login. This makes onboarding new users quick and organized while keeping things secure.

It was clear that the process needed to be more structured so only authorized ICT staff should be able to create records, while departments should have an easy and secure way to confirm repairs.

#### Proposed Solution

The final solution was to build in **authentication** and **email-based confirmation**:

- **Secure login for ICT staff:** Only verified ICT personnel can access the system to create or manage repair records.
    
- **Account management by Head of Hardware:** The Head of Hardware handles new staff accounts, each starting with a temporary password (their surname).
    
- **Email confirmation for departments:** Once a repair is completed, the system sends a confirmation link to the department’s email.
    
- **Departmental feedback:** Departments use that link to mark whether the repair was satisfactory and add their signature.
    
- **Record locking:** After confirmation, the record gets locked and stored securely.
    
- **Notification to ICT staff:** The assigned ICT personnel are notified once the department completes their part.
    

This setup ensures that only authorized people can create or edit records, every confirmation is traceable, and no one can tamper with past entries. Overall, it keeps the system **secure, organized and easy to manage**.