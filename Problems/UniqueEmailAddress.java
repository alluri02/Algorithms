/*

Problem : https://leetcode.com/problems/unique-email-addresses/

For example, in alice@leetcode.com, alice is the local name, and leetcode.com is the domain name.
Besides lowercase letters, these emails may contain '.'s or '+'s.
If you add periods ('.') between some characters in the local name part of an email address, 
mail sent there will be forwarded to the same address without dots in the local name.  
For example, "alice.z@leetcode.com" and "alicez@leetcode.com" forward to the same email address.  
(Note that this rule does not apply for domain names.)
If you add a plus ('+') in the local name, everything after the first plus sign will be ignored. 
This allows certain emails to be filtered, for example m.y+name@email.com will be forwarded to my@email.com.  
(Again, this rule does not apply for domain names.)

It is possible to use both of these rules at the same time.

Given a list of emails, we send one email to each address in the list.  
How many different addresses actually receive mails? 
*/

class UniqueEmailAddress {

    public int numberOfUniqueEmail(String[] emails){
      Set<String> emailSet = new HashSet<>();
      for(String email : emails){
        int index = email.indexOf('@');
        String local = email.substring(0, index);
        String rest = email.substring(index);
        if(local.contains("+")){
          local = local.substring(0, local.indexOf('+'));
        }
        local = local.replaceAll(".","");
        emailSet.add(local+rest);
      }
      return emailSet.size();
    }
}
