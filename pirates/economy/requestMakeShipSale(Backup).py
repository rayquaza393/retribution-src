    def requestMakeShipSale(self, buying, selling, names):
        self.notify.info("requestMakeShipSale: ({0}) ({1}) ({2})".format(buying, selling, names))

        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        
        if not av:
            return

        def sendResponse(resultCode, avId=avId):
            self.sendUpdateToAvatarId(avId, 'makeSaleResponse', [resultCode]) 

        if not len(buying) > 0:
            self.notify.warning("Unable to process ship sale. Received malformed 'requestMakeShipSale' packet")
            sendResponse(RejectCode.TIMEOUT)
            return  

        itemData = buying[0]
        if not itemData:
            self.notify.warning("Unable to process ship sale. Invalid itemData received")
            sendResponse(RejectCode.TIMEOUT)
            return

        shipId = itemData[0]
        requiredGold = EconomyGlobals.getItemCost(shipId)
        if not requiredGold:
            self.notify.warning("Unable to locate price for shipId: %s" % shipId)
            sendResponse(RejectCode.TIMEOUT)
            return   

        requiredGold = requiredGold
        if requiredGold > av.getGoldInPocket():
            sendResponse(0)
            return         

        inv = av.getInventory()
        if not inv:
            self.notify.warning("Unable to locate inventory for avatarId: %s" % avId)
            sendResponse(RejectCode.TIMEOUT)
            return

        resultCode = 0
        availableSlot = -1

        location = inv.findAvailableLocation(InventoryType.NewShipToken, itemId=shipId, count=amount, equippable=True)
        if location != -1:
            availableSlot = location
        else:
            resultCode = RejectCode.OVERFLOW

        if availableSlot != -1:
            success = inv.addLocatable(shipId, availableSlot, 1)
            if success:
                av.takeGold(requiredGold)
                resultCode = 2
        sendResponse(resultCode) 