import concurrent.futures
from smooth import SmoothClient

tasks = [
    """Go to octopus.energy and get a quote for gas + electricity. Use the following information:
    
    - 1, Garlic Row, Cambridge CB5 8HW
    - Medium consumption

    Return the final monthly estimate for all available tariffs.""",
    
    """Search for flights on Google Flights from New York to London, departing tomorrow, coming back in a week. Find the cheapest round-trip option and return:
    - Flight details (airline, flight number, times)
    - Price, duration, and number of stops""",
    
    """Go to https://www.sec.gov/search-filings and search for "Apple Inc".
    
    Find their most recent 10-K filing.
    
    Extract:
    - Filing date
    - Document title
    - Total net sales figure for the most recent fiscal year

    Return the extracted info.""",
    
    """Go to the Calendly billing page in the admin section and find my most recent invoice.
    
    Extract:
    - Invoice date
    - Amount paid
    
    Return this information.""",
    
    """Go to https://london.theaisummit.com/conference-agenda/speakers-2025 and extract information about all speakers. 
    For each speaker, collect:
    - Full name
    - Speaker description
    
    Return the data in JSON format as an array of speaker objects.""",
    
    """Test this flow on apple.com:
    
    1. Navigate to the apple website
    2. Go to the page to buy the latest iphone
    3. Select the basic configuration, black, maximum storage
    4. No trade in
    5. Return the price options""",
    
    """Go to Bill Gates' LinkedIn profile and find his latest article.
    
    Extract:
    - Title of the latest article/post
    - Publication date
    - Brief summary of the content (2-3 sentences)
    - Number of likes/reactions if visible""",
    
    """Search for "Antonio Vespoli Circlemind" on LinkedIn. Find his profile and send a connection request with the message: "Hi Antonio, I love Smooth. Would love to connect!" """
]

def run_task(smooth_client, task_description, device=None):
    """Run a single task and return the recording URL when complete"""
    try:
        run_kwargs = {
            'task': task_description,
            'enable_recording': True
        }
        if device:
            run_kwargs['device'] = device
            
        task = smooth_client.run(**run_kwargs)
        
        result = task.result()
        recording_url = task.recording_url()
        
        return {
            'task': task_description[:50] + "..." if len(task_description) > 50 else task_description,
            'recording_url': recording_url,
            'success': True
        }
    except Exception as e:
        return {
            'task': task_description[:50] + "..." if len(task_description) > 50 else task_description,
            'recording_url': None,
            'success': False,
            'error': str(e)
        }

def main():
    smooth_client = SmoothClient(api_key="cmzr-YOUR_API_KEY")
    
    print(f"Running {len(tasks)} tasks in parallel...")
    
    # Use ThreadPoolExecutor to run tasks in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        # Submit all tasks
        future_to_task = {}
        for i, task in enumerate(tasks):
            # Add device=desktop for specific examples: gov (2), flights (1), conference (4), linkedin bill gates (6)
            device = "desktop" if i in [1, 2, 4, 6] else None
            future_to_task[executor.submit(run_task, smooth_client, task, device)] = task
        
        # Process results as they complete
        for future in concurrent.futures.as_completed(future_to_task):
            result = future.result()
            
            if result['success']:
                print(f"✅ Task completed: {result['task']}")
                print(f"   Recording URL: {result['recording_url']}")
            else:
                print(f"❌ Task failed: {result['task']}")
                print(f"   Error: {result['error']}")
            print("-" * 80)

if __name__ == "__main__":
    main()