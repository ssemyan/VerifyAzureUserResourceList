# VerifyAzureUserResourceList

This python script takes a list of tab separated username/passwords for Azure (in *logins.tsv*), logs in using the [Azure CLI](https://docs.microsoft.com/cli/azure/?view=azure-cli-latest), and pulls a list of the resources in the user's account. This list (types and numbers) is then compared to an expected tab separated list of resources from *expected_resources.tsv*.

Errors are reported if:
- The login is incorrect
- There are duplicate users in the user list
- The overall number of Azure resources in the user's account does not match the expected number
- The count for a type of resource (e.g. Storage Account) does not match what is expected

This tool would be useful when verifying a group of users has the appropriate resources created for them (e.g. for a lab for a training event). 
