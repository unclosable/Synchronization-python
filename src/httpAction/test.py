
from HttpConnect import HttpConnect

if __name__ == "__main__":
    conn = HttpConnect("pms-service.wltest.com")

    response = conn.getresponse("/V2/rights/bd35be89-8657-43"
                                "f1-9257-4b145f424bb6/url?url=eyes.wltest.com/standard?random=0.15766961262436152")

    print(response)
