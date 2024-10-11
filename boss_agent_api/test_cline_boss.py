import vscode
import asyncio

async def test_cline_boss():
    print("Testing ClineBoss extension...")

    # Test plus button
    await vscode.commands.executeCommand('clineBoss.plus')
    
    # Test popout button
    await vscode.commands.executeCommand('clineBoss.popout')
    
    # Test settings button
    await vscode.commands.executeCommand('clineBoss.settings')
    
    # Test history button
    await vscode.commands.executeCommand('clineBoss.history')
    
    # Test send custom message
    await vscode.commands.executeCommand('clineBoss.sendMessage')
    
    # Test export chat history
    await vscode.commands.executeCommand('clineBoss.exportHistory')
    
    # Test update settings
    await vscode.commands.executeCommand('clineBoss.updateSettings')

    print("ClineBoss extension tests completed.")

# Run the test function
asyncio.run(test_cline_boss())
